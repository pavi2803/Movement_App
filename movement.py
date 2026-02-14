"""
✨ Cute Movement Reminder App ✨
A sweet little app to remind you to move and stretch!
(Simplified version - no tkinter needed!)
"""

import pystray
from PIL import Image, ImageDraw
import threading
import time
import random
import platform
import subprocess  # For playing sounds on Mac/Linux


class MovementReminderApp:
    def __init__(self):
        # Settings
        self.interval_minutes = 30  # Default: remind every 30 minutes
        self.is_running = True
        self.is_paused = False
        self.last_reminder_time = time.time()
        self.sound_enabled = True  # Sound on by default!
        
        # Cute reminder messages
        self.messages = [
            "Time to stretch, cutie!",
            "Let's wiggle a bit!",
            "Stand up and shine!",
            "Movement break time!",
            "Time to flutter around!",
            "Stretch those lovely limbs!",
            "Let's get moving, bestie!",
            "Your body will thank you!",
            "Time for a little dance!",
            "Float around for a minute!"
        ]
        
        # Exercise suggestions
        self.exercises = [
            "🙆‍♀️ Reach for the sky - 10 times!",
            "🤸‍♀️ Do 5 gentle stretches",
            "🚶‍♀️ Walk around for 2 minutes",
            "☀️ Look outside the window!",
            "🧘‍♀️ Take 5 deep breaths",
            "🔄 Roll your shoulders - feels amazing!",
            "🤗 Give yourself a hug (you deserve it!)",
            "👣 March in place for 30 seconds",
            "🌊 Gentle side-to-side stretches"
        ]
        

        
        # Create system tray icon
        self.create_tray_icon()
        
        # Start reminder thread
        self.reminder_thread = threading.Thread(target=self.reminder_loop, daemon=True)
        self.reminder_thread.start()
    
    def create_tray_icon(self):
        """Create a system tray icon - uses custom icon if available, otherwise creates a pink heart"""
        # Try to load custom icon first
        try:
            # Put your icon file in the same folder as this script
            # Supported formats: .png, .jpg, .ico
            # Name it "icon.png" or change the filename below
            image = Image.open("fox2.jpg")
            # Resize to appropriate size for tray icon
            image = image.resize((64, 64), Image.Resampling.LANCZOS)
        except FileNotFoundError:
            print("! Custom icon not found, using default pink heart")
            # Create default pink heart icon
            image = Image.new('RGB', (64, 64), color='white')
            dc = ImageDraw.Draw(image)
            
            # Draw a pink heart
            dc.ellipse([10, 15, 30, 35], fill='#FFB6C1')  # Left part of heart
            dc.ellipse([34, 15, 54, 35], fill='#FFB6C1')  # Right part of heart
            dc.polygon([32, 28, 10, 48, 32, 58, 54, 48], fill='#FFB6C1')  # Bottom point
        except Exception as e:
            print(f"! Error loading custom icon: {e}")
            print("! Using default pink heart")
            # Fallback to pink heart
            image = Image.new('RGB', (64, 64), color='white')
            dc = ImageDraw.Draw(image)
            dc.ellipse([10, 15, 30, 35], fill='#FFB6C1')
            dc.ellipse([34, 15, 54, 35], fill='#FFB6C1')
            dc.polygon([32, 28, 10, 48, 32, 58, 54, 48], fill='#FFB6C1')
        
        # Create menu with interval options
        self.update_menu()
        
        self.icon = pystray.Icon("movement_reminder", image, "Movement Reminder 💕", self.menu)
    
    
    def update_menu(self):
        """Update the menu with current settings"""
        self.menu = pystray.Menu(
            pystray.MenuItem("Movement Reminder", lambda: None, enabled=False),
            pystray.MenuItem("⏰ Every 30 minutes", lambda: None, enabled=False),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("🔔 Sound " + ("ON ✓" if self.sound_enabled else "OFF"), self.toggle_sound),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("⏸️ Pause" if not self.is_paused else "▶️ Resume", self.toggle_pause),
            pystray.MenuItem("📊 Check Status", self.show_status),
            pystray.MenuItem("🔔 Alert Now", self.test_reminder),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("❌ Quit", self.quit_app)
        )
    
    def reminder_loop(self):
        """Main loop that checks if it's time to send a reminder"""
        while self.is_running:
            if not self.is_paused:
                current_time = time.time()
                elapsed_minutes = (current_time - self.last_reminder_time) / 60
                
                if elapsed_minutes >= self.interval_minutes:
                    self.send_reminder()
                    self.last_reminder_time = current_time
            
            time.sleep(10)  # Check every 10 seconds
    
    def send_reminder(self):
        """Send a cute reminder notification with sound!"""
        title = random.choice(self.messages)
        message = random.choice(self.exercises)
        
        # Play notification sound based on OS
        if self.sound_enabled:
            try:
                system = platform.system()
                if system == "Darwin":  # macOS
                    # Play the default macOS notification sound (the "ting!")
                    subprocess.run(["afplay", "/System/Library/Sounds/Glass.aiff"], check=False)
                elif system == "Windows":
                    import winsound
                    winsound.MessageBeep(winsound.MB_ICONASTERISK)
                elif system == "Linux":
                    # Try to play a sound on Linux
                    subprocess.run(["paplay", "/usr/share/sounds/freedesktop/stereo/message.oga"], check=False)
            except:
                pass  # If sound fails, continue anyway
        
        # Show notification
        self.icon.notify(title=title, message=message)
    
    def test_reminder(self):
        """Send a test reminder immediately"""
        self.send_reminder()
    
    def toggle_pause(self):
        """Pause or resume reminders"""
        self.is_paused = not self.is_paused
        self.update_menu()
        self.icon.menu = self.menu
        
        status = "paused ⏸️" if self.is_paused else "resumed ▶️"
        self.icon.notify(
            title=f"Movement Reminder {status}",
            message="Right-click the tray icon to change this anytime!"
        )
    
    def show_status(self):
        """Show current status via notification"""
        elapsed = (time.time() - self.last_reminder_time) / 60
        next_reminder = max(0, self.interval_minutes - elapsed)
        
        status_text = f"""⏰ Reminds every 30 minutes
⏳ Next in: {int(next_reminder)} min
{"⏸️ PAUSED" if self.is_paused else "✅ Active"}"""
        
        self.icon.notify(
            title="📊 Current Status",
            message=status_text
        )
    
    def toggle_sound(self):
        """Toggle notification sound on/off"""
        self.sound_enabled = not self.sound_enabled
        self.update_menu()
        self.icon.menu = self.menu
        
        status = "ON 🔔" if self.sound_enabled else "OFF 🔇"
        self.icon.notify(
            title=f"Sound {status}",
            message="Notification sounds are now " + ("enabled! 🎵" if self.sound_enabled else "disabled.")
        )
    
    def quit_app(self):
        """Quit the application"""
        self.is_running = False
        self.icon.stop()
    
    def run(self):
        """Run the system tray app"""
        # Show welcome notification
        self.icon.notify(
            title="Movement Reminder Started!",
            message=f"I'll remind you every 30 minutes to move and stretch! Right-click the pink heart icon for options. ✨"
        )
        self.icon.run()


if __name__ == "__main__":
    print("✨ Starting Movement Reminder App...")
    print("💕 Look for the pink heart icon in your system tray!")
    print("🎀 Right-click it to access settings and options.")
    print("")
    
    app = MovementReminderApp()
    app.run()