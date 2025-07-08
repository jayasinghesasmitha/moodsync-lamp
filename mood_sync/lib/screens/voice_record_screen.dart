import 'package:flutter/material.dart';
import 'package:permission_handler/permission_handler.dart';
import 'package:path_provider/path_provider.dart';
import 'package:path/path.dart' as path;
import 'package:record/record.dart';

class VoiceRecordScreen extends StatefulWidget {
  const VoiceRecordScreen({super.key});

  @override
  State<VoiceRecordScreen> createState() => _VoiceRecordScreenState();
}

class _VoiceRecordScreenState extends State<VoiceRecordScreen> {
  final AudioRecorder _recorder = AudioRecorder();
  bool _hasPermission = false;
  bool _isRecording = false;
  bool _isLoading = false;
  String _recordingStatus = 'Press start to record';
  String? _recordedFilePath;

  @override
  void initState() {
    super.initState();
    _checkPermission();
  }

  @override
  void dispose() {
    _recorder.dispose();
    super.dispose();
  }

  Future<void> _checkPermission() async {
    setState(() => _isLoading = true);
    try {
      final status = await Permission.microphone.status;
      if (!status.isGranted) {
        await _requestPermission();
      } else {
        setState(() => _hasPermission = true);
      }
    } catch (e) {
      _showError('Failed to check permissions: $e');
    } finally {
      setState(() => _isLoading = false);
    }
  }

  Future<void> _requestPermission() async {
    try {
      final status = await Permission.microphone.request();
      setState(() {
        _hasPermission = status.isGranted;
      });
      if (!status.isGranted) {
        _showError('Microphone permission is required for recording');
      }
    } catch (e) {
      _showError('Failed to request permission: $e');
    }
  }

  Future<void> _startRecording() async {
    if (!_hasPermission || _isRecording) return;

    setState(() => _isLoading = true);
    
    final dir = await getTemporaryDirectory();
    final filePath = path.join(
      dir.path,
      'recording_${DateTime.now().millisecondsSinceEpoch}.m4a',
    );

    try {
      await _recorder.start(
        const RecordConfig(
          encoder: AudioEncoder.aacLc,
          bitRate: 128000,
          sampleRate: 44100,
        ),
        path: filePath,
      );

      setState(() {
        _recordingStatus = 'Recording...';
        _isRecording = true;
        _recordedFilePath = filePath;
      });
    } catch (e) {
      _showError('Failed to start recording: $e');
    } finally {
      setState(() => _isLoading = false);
    }
  }

  Future<void> _stopRecording() async {
    if (!_isRecording) return;

    setState(() => _isLoading = true);
    
    try {
      final savedPath = await _recorder.stop();

      setState(() {
        _recordingStatus = 'Recording saved to:\n${path.basename(savedPath ?? '')}';
        _isRecording = false;
        _recordedFilePath = savedPath;
      });

      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Recording saved to ${path.basename(savedPath ?? '')}'),
          duration: const Duration(seconds: 2),
        ),
      );
    } catch (e) {
      _showError('Failed to stop recording: $e');
    } finally {
      setState(() => _isLoading = false);
    }
  }

  void _showError(String message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(message),
        backgroundColor: Colors.red,
        duration: const Duration(seconds: 3),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFf9fafa),
      appBar: AppBar(
        title: const Text('Voice Recorder'),
        actions: [
          if (!_hasPermission)
            IconButton(
              icon: const Icon(Icons.settings),
              onPressed: () => openAppSettings(),
              tooltip: 'Open settings to grant permission',
            ),
        ],
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : !_hasPermission
              ? Center(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      const Text(
                        'Microphone permission required',
                        style: TextStyle(fontSize: 18),
                      ),
                      const SizedBox(height: 20),
                      ElevatedButton(
                        onPressed: _requestPermission,
                        child: const Text('Grant Permission'),
                      ),
                    ],
                  ),
                )
              : Center(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Container(
                        width: 300,
                        height: 300,
                        decoration: BoxDecoration(
                          color: _isRecording ? Colors.red[800] : Colors.black,
                          borderRadius: BorderRadius.circular(10),
                        ),
                        child: Center(
                          child: Padding(
                            padding: const EdgeInsets.all(16.0),
                            child: Text(
                              _recordingStatus,
                              style: const TextStyle(
                                color: Colors.white,
                                fontSize: 18,
                                fontWeight: FontWeight.bold,
                              ),
                              textAlign: TextAlign.center,
                            ),
                          ),
                        ),
                      ),
                      const SizedBox(height: 30),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          ElevatedButton.icon(
                            icon: const Icon(Icons.mic),
                            label: const Text('Start'),
                            onPressed: _isRecording ? null : _startRecording,
                            style: ElevatedButton.styleFrom(
                              backgroundColor: Colors.green,
                              foregroundColor: Colors.white,
                              padding: const EdgeInsets.symmetric(
                                  horizontal: 24, vertical: 12),
                            ),
                          ),
                          const SizedBox(width: 20),
                          ElevatedButton.icon(
                            icon: const Icon(Icons.stop),
                            label: const Text('Stop'),
                            onPressed: _isRecording ? _stopRecording : null,
                            style: ElevatedButton.styleFrom(
                              backgroundColor: Colors.red,
                              foregroundColor: Colors.white,
                              padding: const EdgeInsets.symmetric(
                                  horizontal: 24, vertical: 12),
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 20),
                      if (_recordedFilePath != null)
                        Text(
                          'Last recording: ${path.basename(_recordedFilePath!)}',
                          style: const TextStyle(fontStyle: FontStyle.italic),
                        ),
                      const SizedBox(height: 20),
                      TextButton(
                        onPressed: () => Navigator.pushNamed(context, '/camera'),
                        child: const Text('Go to Camera Screen'),
                      ),
                    ],
                  ),
                ),
    );
  }
}