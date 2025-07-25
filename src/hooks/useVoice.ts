/**
 * @file useVoice.ts
 * @description Custom hook for voice recording and recognition functionality
 */

import { useState, useCallback, useRef } from 'react';
import { VoiceState } from '../providers/VoiceProvider';

export const useVoice = (): VoiceState & {
  startListening: () => void;
  stopListening: () => void;
  isListening: boolean;
  transcript: string;
  requestPermission: () => Promise<void>;
} => {
  const [isRecording, setIsRecording] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [hasPermission, setHasPermission] = useState<boolean | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [stream, setStream] = useState<MediaStream | null>(null);
  const [audioData, setAudioData] = useState<Blob | null>(null);
  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState('');
  const recognitionRef = useRef<any>(null);

  const requestPermission = useCallback(async () => {
    try {
      const mediaStream = await navigator.mediaDevices.getUserMedia({ audio: true });
      setHasPermission(true);
      setStream(mediaStream);
      setError(null);
    } catch (err) {
      setHasPermission(false);
      setError(err instanceof Error ? err.message : 'Failed to get microphone permission');
    }
  }, []);

  const startListening = useCallback(() => {
    if (!('webkitSpeechRecognition' in window)) {
      setError('Speech recognition is not supported in this browser.');
      return;
    }
    const recognition = new (window as any).webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.onstart = () => {
      setIsListening(true);
      setError(null);
    };
    recognition.onresult = (event: any) => {
      let finalTranscript = '';
      for (let i = event.resultIndex; i < event.results.length; ++i) {
        finalTranscript += event.results[i][0].transcript;
      }
      setTranscript(finalTranscript);
    };
    recognition.onerror = (event: any) => {
      setError(`Error occurred in recognition: ${event.error}`);
      setIsListening(false);
    };
    recognition.onend = () => {
      setIsListening(false);
    };
    recognition.start();
    recognitionRef.current = recognition;
  }, []);

  const stopListening = useCallback(() => {
    if (recognitionRef.current) {
      recognitionRef.current.stop();
      recognitionRef.current = null;
    }
    setIsListening(false);
  }, []);

  return {
    isRecording,
    isProcessing,
    hasPermission,
    error,
    stream,
    audioData,
    startListening,
    stopListening,
    isListening,
    transcript,
    requestPermission,
  };
}; 