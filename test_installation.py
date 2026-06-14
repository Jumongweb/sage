#!/usr/bin/env python3
"""
Quick test script to verify all dependencies are installed correctly.
"""

import sys

def test_imports():
    """Test if all required modules can be imported."""
    print("Testing dependencies...\n")
    
    tests = [
        ("pyttsx3", "Text-to-speech engine"),
        ("speech_recognition", "Speech recognition"),
        ("pyaudio", "Audio I/O"),
        ("pvporcupine", "Wake word detection (Porcupine)"),
        ("pyautogui", "GUI automation"),
    ]
    
    failed = []
    
    for module_name, description in tests:
        try:
            __import__(module_name)
            print(f"✅ {description} ({module_name})")
        except ImportError as e:
            print(f"❌ {description} ({module_name}) - FAILED")
            print(f"   Error: {e}")
            failed.append(module_name)
    
    print("\n" + "="*50)
    
    if failed:
        print(f"\n❌ {len(failed)} module(s) failed to import:")
        for module in failed:
            print(f"   - {module}")
        print("\nPlease install missing dependencies:")
        print("   pip install -r requirements.txt")
        return False
    else:
        print("\n✅ All dependencies are installed correctly!")
        print("\nYou can now run: python3 main.py")
        return True

def test_microphone():
    """Test if microphone is accessible."""
    print("\nTesting microphone access...")
    try:
        import pyaudio
        pa = pyaudio.PyAudio()
        
        # Try to get default input device
        default_input = pa.get_default_input_device_info()
        print(f"✅ Microphone detected: {default_input['name']}")
        
        pa.terminate()
        return True
    except Exception as e:
        print(f"⚠️  Microphone test failed: {e}")
        print("   Make sure microphone permissions are granted in System Preferences")
        return False

def test_porcupine():
    """Test if Porcupine can be initialized."""
    print("\nTesting Porcupine wake word engine...")
    try:
        import pvporcupine
        porcupine = pvporcupine.create(keywords=['hey siri'])  # Using as placeholder for "Hey Sage"
        print(f"✅ Porcupine initialized successfully")
        print(f"   Sample rate: {porcupine.sample_rate} Hz")
        print(f"   Frame length: {porcupine.frame_length}")
        print(f"   Note: Currently using 'Hey Siri' as placeholder for 'Hey Sage'")
        porcupine.delete()
        return True
    except Exception as e:
        print(f"❌ Porcupine test failed: {e}")
        return False

if __name__ == "__main__":
    print("="*50)
    print("  SAGE INSTALLATION TEST")
    print("="*50 + "\n")
    
    success = True
    
    # Test imports
    if not test_imports():
        success = False
    
    # Test microphone
    if not test_microphone():
        success = False
    
    # Test Porcupine
    if not test_porcupine():
        success = False
    
    print("\n" + "="*50)
    
    if success:
        print("\n🎉 All tests passed! Sage is ready to use!")
        print("\nRun: python3 main.py")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")
        sys.exit(1)
