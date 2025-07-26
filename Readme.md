
# New NEV Client

## 👤 **Author**

[SAMAIN Luc](https://github.com/LucSAMAIN)

## 📝 **Description**

This project is a modern version of the NEV client, originally developed in 2017 by Dr. Kohno. It is used in the Kohno Lab to support research on neuromimetic systems.

## 🚀 **How to Run**

### 💻 **Debian Setup**

1.  **Set up the environment and install dependencies:**
    For a standard installation, use a virtual environment to avoid installing the package globally.

    ```bash
    python -m venv .env
    source .env/bin/activate
    pip install .
    ```

2.  **Run the client:**

    ```bash
    python -m nevclient
    ```

### 🪟**Windows Setup**
1.  **Set up the environment and install dependencies:**
    For a standard installation, use a virtual environment to avoid installing the package globally.

    ```powershell
    python -m venv .env
    source .env/Scripts/Activate.ps1
    pip install .
    ```

2.  **Run the client:**

    ```powershell
    python -m nevclient
    ```



### 👨‍💻 **Development Mode**

If you want to run the client in **development (editable) mode**, follow the same steps as above, but use the following `pip` command for installation. This allows your changes to the source code to be reflected immediately without reinstalling.

```bash
pip install -e .
```


## 📂 **Project Structure**

### Tree diagram

The project is organized into several key directories:

  * `nevclient/`: The main package for the application.
      * `__main__.py`: The entry point for the application.
      * `Controller.py`: The central controller that manages the application's logic and data flow between the model and view.
      * `factories/`: Contains factory classes for creating complex objects.
      * `model/`: Defines the data structures for the application, including hardware representations (`DAQMX`, `NISCOPE`), configuration data (`PSA`, `Pulse`, `Parameters`), and various enums.
      * `services/`: Provides services for communication, data parsing, data manipulation, and running processes.
      * `utils/`: Contains utility classes such as the `TCPClient`, `Logger`, and `CSVWorker`.
      * `views/`: Contains the GUI components built with `wxPython`.

### Architecture and workflow

To understand how the app is initialized, launched and handled the events with the user you should follow these steps:

  1. The `__main__.py` python file is the entry point of the application. It creates the main used instances during runtime or initialization phase of the app. It then passes these instances as arguments to an instance of the `Controller` class. After initialization of the controller, the `wxPython` main loop starts.

  2. Entering runtime, the `wx` main loop takes the lead. Everytime a user interacts with a widget that is binded to a handling function (usually called *'event handler'* in the code), the `wx` main loop invokes this  event and executes the associated code.

  3. I tried to follow a certain code architecture while building the project. A commonly-known architecture for GUI of web apps is the MVC (Model View Controller) architecture. It tries to seperate the actual data (the model) from the displayed view for the final user (the view) and from the logic (the controller) behind interactions between the two other parts (the model and the view).
  As much as I could, I tried to make the views as *'dumb'* as possible. They should only be responsible of the display layouts and final looks of the application. I tried to make them unaware of the logic and processes to execute when the user decide to interact with them.
  When an event is triggered by the user, the view redirects it, with the corresponding information (button clicked, new value, etc.), to its instance of the `Controller` class. You can see that most of the written coding lines composing the `Controller` class are used to define the different event handlers from the all the views.
  Whenever the logic for an event handler becomes too complex or long, the controller calls an associated service to manage it. It allows the controller to stay *simple* to a certain extent.
  The model class is used to store information both about hardware and configuration settings displayed on the GUI. I tried to make the different classes that are defined in this part of the code designed as simple data containers. Because the model's classes only store useful data information, they are unaware of the executed algorithm on them or even the views using their different attributes to display things.  

### Utils

The utils directory defines several useful classes such as the `TCPClient` to communicate with the backend server, or the `Theme` file defining useful functions to define themes throughout the different veiws. The defined files inside this module are not following the MVC architecture. They are built to be useful and easy to understand by following non-strict design rules.  


## 🛠️ **Developer Documentation**

This section contains technical notes, API specifications, and other details relevant for developers.


### 🎥 **Video Example**

A video demonstrating the **OLD** client's usage is available on [Google Drive](https://drive.google.com/file/d/1KK7XNl8c_oym9D4XNb7_BlA7rHWUiEnB/view).

### **CSV Attribute Rules**

The first line of a CSV file is reserved for attribute definitions. Attribute names must be prefixed with a `#`.

  * `#ID` (**Required**): Parameter ID number.
  * `#COMMENT` (Optional): Comment text.
  * `#DEV` (**Required**): Device name as registered in the PXI system.
  * `#CH` (**Required**): Channel type and number (e.g., `AO-0`, `DO-3`).
  * `#PIN` (Optional)
  * `#LABEL` (**Required**): Parameter name.
  * `#NCMODE` (**Required**): Null-cline-mode setting.

### **Terminology**

**Hardware**

  * **DAQmx**: Data Acquisition Multifunction devices.
  * **Input Types**:
      * **SAO**: Static Analog Output
      * **SDO**: Static Digital Output
      * **DAO**: Dynamic Analog Output
      * **DDO**: Dynamic Digital Output
  * **NSU**: NIScope Union

**Software**

  * **PSA**: Parameter Sweep Analysis

### **API Calls**

**GET DAQMXINFO**

  * **Response**:
    ```
    #DAQMXINFO
    SAO[device-info]…
    DAO[device-info]…
    SDO[device-info]…
    #OK
    ```
  * **Device Info Format**: `[taskNo, deviceName, model, nChan, oneShot/L_data, freq, state]`

**GET NISCOPEINFO**

  * **Response**:
    ```
    #NISCOPEINFO
    [<device1-info> <device2-info>...]
    #OK
    ```
  * **Device Info Format**: `[slot, deviceName, modelName, nChannels, chassis, serial]`

**GET NSU NUM**

  * **Response**:
    ```
    #NSUNUM
    <number-of-unions>
    #OK
    ```

**GET NSU TRIG unionId**

  * **Response**:
    ```
    #NSUTRIG unionNo
    <trig> [refPosition trigger_type triggerSource trigger_device triggerLevel trigger_slope trigger_coupling triggerHoldoff triggerDelay]
    #OK
    ```

**GET NSU CHAN unionId**

  * **Response**:
    ```
    #NSUCHAN <unionNo>
    <N_channels> [<range1> <coup1>][<range2> <coup2>]...[<rangeN> <coupN>]
    #OK
    ```

**GET NSU DLEN unionId**

  * **Response**:
    ```
    #NSUDLEN unionNo
    <dlen> [deviceDLen0 deviceDLen1 ...]
    #OK
    ```

**SET SAO/SDO**

  * **Command**: `SET SAO/SDO TaskId value value ... value`

**SET DAO/DDO**

  * This is a two-part command:
    1.  **Handshake**: `SET DAO/SDO taskId chStart`
    2.  **Data Sending**: `[value value] [value] [value ... value]`

**SET DAO DLEN/FREQ**

  * **Command**: `SET DAO DLEN/FREQ <device id> <int/float value>`
  * **Response**: `#OK`

**SET PSA**

  * **Command**: `SET PSA unionNo [(SAO|DAO|SDO) device-idx channel-id] [start end steps] <skip-samples>`

**GET PSA DATA**

  * **Command**: `GET PSA DATA <start>-<stop>` (where `start` and `stop` are point indices)
  * **Response**:
    ```
    #PSADATA <start> <stop>
    <sweepValue> [<value> <value> ...]
    <sweepValue> ...
    #OK
    ```

### **Global Comments & Known Issues**

  * The `<trig>` value from the `GET NSU TRIG` response is currently skipped during parsing. This might be why `SET NSU TRIG` is not sent when updating the backend.
  * There's an inconsistency where a `wx.SpinCtrlDouble` widget (intended for float values) is also used for integer values (e.g., the 'steps' control in the sweeper panel).
  * It is unclear how PSA sweeper value should be handled. In dummy data, the mean value is used as a placeholder.
  * The purpose of the `"stim"` attribute for static devices is not well understood and so never used. In the current version, stimuli/pulses only affect dynamic devices.
  * Many processes, such as the `SET PSA` command and CSV parameter loading, rely heavily on the order in which items are loaded.
  * Pulse configuration could be generalized, but the event handlers (`OnChangingAmp1`, `OnChangingAmp2`, etc.) are currently implemented as dedicated functions, which limits flexibility.

