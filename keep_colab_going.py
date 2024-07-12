from IPython.display import Javascript
import threading
import time

n = 0

def keep_colab_alive():
    global n  # Declare n as global to modify it inside the function
    while True:
        print(f"{n} minutes alive")
        n += 1
        display(Javascript('''
        function ClickConnect(){
            console.log("Clicked on connect button");
            document.querySelector("colab-connect-button").click()
        }
        ClickConnect();
        '''))
        time.sleep(60)  # Execute every minute

# Create a thread to run keep_colab_alive function
alive_thread = threading.Thread(target=keep_colab_alive)
alive_thread.start()

# You can continue with your main script here or interact with other cells
