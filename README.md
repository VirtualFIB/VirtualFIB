# liftout-animator
Blender application template to animate in-situ liftout. Also includes Stage Simulator, which aims to help understanding sample orientation in triple-beam instruments.

## How to run

Liftout-Animator (LOA) builds on the Open-Source software Blender, which provides the toolbox to do 3D operations and full freedom to change anything. To install LA we first need to install blender:

1. Download and install [Blender](https://www.blender.org/download/). This version was last tested on Blender version 2.91.2 but should be stable for future minor revisions.

2. Download .zip of LOA code from this repository.

3. Install and run Blender, then click the blender icon in the top left toolbar and select Install Application Template

4. Select the downloaded .zip and install, then restart Blender.

## Usage

After install, when you now open Blender the Splash screen should have a `...` field where you can select Liftout Animator.

![Screenshot: Splash screen](/doc_screenshots/doc_splash1.jpg?raw=true "Splash screen")

Alternatively, press `ctrl+n` for a new file and select Liftout Animator. This will load the default LOA file and control window.

In its current incarnation, LOA has two main parts: Liftout Animator and Stage Simulator:
 - In Liftout Animator, the result of different stage rotation, stage tilt and liftout needle rotation can be visualized for cross-section and/or plan-view lamellas.
 - In Stage Simulator, the stage can be moved around interactively and seen either freely (use the middle mouse button to orbit the view) or from the view of either beam.

The file can be saved, rendered and exported either as animations or still images, and all of Blenders power is available for those who seek it, but to keep the interface from being overwhelming the goal is to have as much complexity as possible hidden by default, with most relevant settings accesible in the Liftout Animator and Stage Simulator control panels.

### Liftout Animator Window:

When opening a new LOA file, the default view should be a 3D view of a lamella and lift-out needle:

![Screenshot: LOA](/doc_screenshots/doc_loa1.jpg?raw=true "LOA 1")

To orbit around in 3D in Blender, hold down the middle mouse button or use the XYZ axes next to the panel in the upper right part of the screen. The actual controls for liftout have been collected in a single panel and are as follows:

<img align="left" width="250" src="/doc_screenshots/doc_loa2.jpg">

 - __Stage Rotation/Stage Tilt/Needle Rotation:__ These are the degrees of freedom for liftout: You can control the stage rotation and tilt axis when lifting out, as well as the rotation around the liftout needle axis.
 - __Play/Pause:__ Starts and stops the animation.
 - __Animate:__ Create and run the animation with above values.
 - __Lamella type (Cross-section/Plan-view):__ Switch between two different lamella configurations
 - __Liftout mode (Animation/Live preview):__ In Animation, set the desired values and press __Animate__ to see the steps. In Live preview, the animation jumps directly to the last frame and updates live as values change, letting you directly see the impact of each degree of freedom on the final lamella orientation.
 - __Reset Lamella Rotation:__ Remove any pre-tilt from the lamella
 - __Restore Liftout Defaults:__ Should change any animation values back to default.
 - __Change to Stage Simulator:__ Change mode, scene and workspace to the Stage Simulator (below).
 - __Animation options:__ Click to expand with multiple behind-the-scenes options to tweak the animation or switch granularly between Animation or Live Preview behaviors.

### Stage Simulator Window:

- Clicking the __Change to Stage Simulator__ button in the Liftout animator will bring you to the Stage Simulator:

![Screenshot: StageSim](/doc_screenshots/doc_stagesim1.jpg?raw=true "StageSim 1")

This model is meant as an aid to navigating the stage in 3D, especially in newer triple-beam systems where hard-to-image-with beams like a laser need to be aligned. A pre-tilted stub with 45 and 60 degree surfaces can be moved using 5-axis controls that should closely mirror those of most FIB systems. The eucentric height is set to 0 in this space, and coincidence for all beams is at (0,0,0). Controls for the Stage Simulator panel are:

<img align="left" width="250" src="/doc_screenshots/doc_stagesim2.jpg">

- __Stage X/Y/Z/R/T:__ Common control axes for FIB stages.
- __Zero Stage:__ Set all axes to 0
- __Go to viewpoint (e/i/laser):__ Show the (orthographic) view for each beam. Current angles between beams are 52 degrees between electron and ion beams, and 60 degrees between electron and laser beams.
- __Change to Liftout Animator:__ Go back to the Liftout Animator.

## How to contribute

To change stuff and update the template, the whole repository can be cloned and worked with directly in the Blender Application Template folder, restarting Blender after changes to check every thing is working. However, the correct folder varies from system to system and will not be created before an application template is installed. Therefore, to make any changes, the easiest way to get up to speed is the following:

1. Install and check LA is working as explained above (Blender automatically creates the right folders in the right places).

2. Navigate to the liftout-animator application template folder. The precise location varies with your system and is detailed [here](https://docs.blender.org/manual/en/latest/advanced/app_templates.html) in the Blender documentation. On Windows, it should be **Username**/AppData/Roaming/Blender Foundation/Blender/**Blender version**/scripts/startup/bl_app_templates_user.

3. Close Blender if you have it open, and delete the liftout-animator folder. Now you can clone the repository to bl_app_templates_user and the next time you open blender it should automatically detect the template.

### Useful links

 - [On blender's application templates](https://docs.blender.org/manual/en/latest/advanced/app_templates.html)
 - [Where the application template can be found on your system](https://docs.blender.org/manual/en/latest/advanced/blender_directory_layout.html#blender-directory-layout)
 - [Blender Add-on tutorial](https://docs.blender.org/manual/en/latest/advanced/app_templates.html)
 - [HDRI Haven for HDRI maps](https://hdrihaven.com/)


