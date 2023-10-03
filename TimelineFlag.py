# API documentation: https://resolve.cafe/developers/scripting/

# Define element IDs
winID = "com.blackmagicdesign.resolve.MyComparisonWindow"
trackSelectionID = "TrackSelection"
propertySelectionID = "StringSelection"
operatorID = "ComparisonSelection"
numberInputID = "NumberInput"
colorID = "ColorSelection"
submitID = "SubmitButton"

# Gather project
pm = resolve.GetProjectManager()
p = pm.GetCurrentProject()
tl = p.GetCurrentTimeline()
tl_items_for_properties = tl.GetItemListInTrack("video", 1)
all_properties = list(tl_items_for_properties[0].GetProperty().keys())

# Count tracks
video_track_count = tl.GetTrackCount("video")
tracks = []
for track in range(video_track_count):
    tracks.append("Video " + str(track+1))

ui = fusion.UIManager
dispatcher = bmd.UIDispatcher(ui)

# Check for an existing instance of the window
win = ui.FindWindow(winID)
if win:
    win.Show()
    win.Raise()
    sys.exit()

# Define the window UI layout
win = dispatcher.AddWindow({
    'ID': winID,
    'Geometry': [100, 100, 170, 300],
    'WindowTitle': "Flag clips"
},
ui.VGroup([
    ui.Label({'Text': "Track:"}),
    ui.ComboBox({
        'ID': trackSelectionID,
    }),
    ui.Label({'Text': "Property:"}),
    ui.ComboBox({
        'ID': propertySelectionID,
    }),
    ui.Label({'Text': "Operator:"}),
    ui.ComboBox({
        'ID': operatorID,
    }),
    ui.Label({'Text': "Integer:"}),
    ui.LineEdit({
        'ID': numberInputID,
        'MinimumSize': [80, 25],  # Width of 80 pixels, default height
        'MaximumSize': [170, 25],  # Width of 80 pixels, default height
        'Font': ui.Font({'Family': "Sans Mono", 'PixelSize': 12, 'MonoSpaced': True, 'StyleStrategy': {'ForceIntegerMetrics': True}}),
    }),
    ui.Label({'Text': "Color:"}),
    ui.ComboBox({
        'ID': colorID,
    }),
    ui.HGroup([  # Center-align the button using an HGroup with spacers
        ui.Button({
            'ID': submitID,
            'Text': "Flag",
           'MinimumSize': [150, 25],  # An example size; adjust as needed
           'MaximumSize': [170, 30]
        }),
        ui.HGap(0, 0.5),  # Decrease or maintain weight
    ]),
    ui.VGap(10),
])
)

# Add items to the ComboBoxes
trackDropDown = win.Find(trackSelectionID)
trackDropDown.AddItems(tracks)

propertyDropDown = win.Find(propertySelectionID)
propertyDropDown.AddItems(all_properties)

operatorDropDown = win.Find(operatorID)
operatorDropDown.AddItems(["equals", "does not equal", "is greater than", "is less than"])

colorDropDown = win.Find(colorID)
colorDropDown.AddItems(["Blue", "Cyan", "Green", "Yellow", "Red", "Pink", "Purple", "Fuchsia", "Rose", "Lavender", "Sky", "Mint", "Lemon", "Sand", "Cocoa", "Cream"])


# Event handlers
def OnClose(ev):
    dispatcher.ExitLoop()

def OnSubmit(ev):
    selected_track = win.Find(trackSelectionID).CurrentText
    selected_property = win.Find(propertySelectionID).CurrentText
    selected_operator = win.Find(operatorID).CurrentText
    selected_color = win.Find(colorID).CurrentText
    entered_number = win.Find(numberInputID).Text

    try:
        entered_number = float(entered_number)
    except ValueError:
        print("Please enter a valid number.")
        return

    # Here, you can add code to process the gathered values.
    print(f"Selected track: {selected_track}")
    print(f"Selected property: {selected_property}")
    print(f"Selected operator: {selected_operator}")
    print(f"Entered number: {entered_number}")
    print(f"Selected color: {selected_color}")

    tl_items = tl.GetItemListInTrack("video", int(selected_track.split()[1]))

    if selected_operator == "equals":
        results = [item for item in tl_items if item.GetProperty()[selected_property] == entered_number]
    elif selected_operator == "does not equal":
        results = [item for item in tl_items if item.GetProperty()[selected_property] != entered_number]
    elif selected_operator == "is greater than":
        results = [item for item in tl_items if item.GetProperty()[selected_property] > entered_number]
    elif selected_operator == "is less than":
        results = [item for item in tl_items if item.GetProperty()[selected_property] < entered_number]

    # Add flags
    for clip in results: clip.AddFlag(selected_color)

# Assign event handlers
win.On[winID].Close = OnClose
win.On[submitID].Clicked = OnSubmit

# Show the window and run the dispatcher loop
win.Show()
dispatcher.RunLoop()
