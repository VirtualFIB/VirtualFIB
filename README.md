# VirtualFIB
VirtualFIB is a Blender application template, simplifying and automating what we need to simulate a few different situations you might encounter when doing FIB technique development. It currently includes the Liftout Animator to animate *in situ* liftout, the Post Welder which is a copy of the Liftout Animator with a controllable half-grid post in the chamber, and finally the Stage Simulator, which aims to help understanding sample orientation in triple-beam instruments.

## Table of contents
* [Requirements](#requirements)
* [How to install](#how-to-install)
* [Usage](#usage)
* [Liftout Animator Window](#liftout-animator-window)
* [Stage Simulator Window](#stage-simulator-window)
* [Uh oh, I messed something up](#uh-oh-i-messed-something-up)
* [How to contribute](#how-to-contribute)
* [Useful links](#useful-links)

## Requirements

This version was built for Blender version 2.93, which is compatible with most operating systems ([Blender requirements](https://www.blender.org/download/requirements/)), but has limited compatability with older macOS versions (requires 10.13 or newer). 

It has also been tested with the 2.83 [Long Term Support branch](https://www.blender.org/download/lts/) (2.83.16), which supports macOS 10.12 and above. Note: If using 2.83 LTS the stage tilt axis may be reversed. Counter this by checking the `Reverse stage tilt` option in the Animation Options.

This application template is generally not compatible with Blender 2.79 or below.

## How to install

VirtualFIB builds on the Open-Source 3D creation suite Blender, which provides the toolbox to do 3D operations and full freedom to change anything. To install LA we first need to install blender:

1. Download and install [Blender](https://www.blender.org/download/). This version was last tested on Blender version 2.93.1 but should be stable for future minor revisions.

2. Download .zip of VirtualFIB code from this repository.

3. Install and run Blender, then click the blender icon in the top left toolbar and select Install Application Template

4. Select the downloaded .zip and install, then restart Blender.

## Usage

After installation, when you open Blender the [Splash Screen](https://docs.blender.org/manual/en/dev/interface/window_system/splash.html) should now on the left, under New File, have a `...` field where you can select VirtualFIB as shown below.

![Screenshot: Splash screen](/doc_screenshots/doc_splash_1.jpg?raw=true "Splash screen")

Alternatively, press `ctrl+N` for a new file and select VirtualFIB. This will load the default VirtualFIB file and control window.

In its current incarnation, VirtualFIB has three main parts: Liftout Animator, Post Welder and Stage Simulator:
 - In Liftout Animator, the result of different stage rotation, stage tilt and liftout needle rotation can be visualized for cross-section and/or plan-view lamellas.
 - In Post Welder, you have the full Liftout Animator but with an added half-grid post in the chamber. Post Welder is intended to let you visualize how you can weld your lamella to the post.
 - In Stage Simulator, the stage can be moved around interactively and seen either freely (use the middle mouse button to orbit the view) or from the view of either beam.

The file can be saved, rendered and exported either as animations or still images, and all of Blenders power is available for those who seek it, but to keep the interface from being overwhelming the goal is to have as much complexity as possible hidden by default, with most relevant settings accesible in the Liftout Animator and Stage Simulator control panels.

### Liftout Animator Window:

When opening a new VirtualFIB file, the default view should be a 3D view of a lamella and lift-out needle:

![Screenshot: VirtualFIB](/doc_screenshots/doc_loa_1.jpg?raw=true "LOA 1")

To orbit around in 3D in Blender, hold down the middle mouse button or use the XYZ axes next to the panel in the upper right part of the screen. The actual controls for liftout have been collected in a single panel and are as follows:

<img align="left" width="250" src="/doc_screenshots/doc_loa_2.jpg">

 - __Stage Rotation/Stage Tilt/Needle Rotation:__ These are the degrees of freedom for liftout: You can control the stage rotation and tilt axis when lifting out, as well as the rotation around the liftout needle axis.
 - __Play/Pause:__ Starts and stops the animation.
 - __Animate:__ Create and run the animation with above values.
 - __Lamella type (Cross-section/Plan-view):__ Switch between two different lamella configurations
 - __Liftout mode (Animation/Live preview):__ In Animation, set the desired values and press __Animate__ to see the steps. In Live preview, the animation jumps directly to the last frame and updates live as values change, letting you directly see the impact of each degree of freedom on the final lamella orientation.
 - __Reset Lamella Rotation:__ Remove any pre-tilt from the lamella
 - __Restore Liftout Defaults:__ Should change any animation values back to default.
 - __Change to Stage Simulator:__ Change mode, scene and workspace to the Stage Simulator (below).
 - __Animation options:__ Click to expand with multiple behind-the-scenes options to tweak the animation or switch granularly between Animation or Live Preview behaviors.

### Post Welder

- Post Welder includes the Beam View and Change to Module menus, the PostSim Liftout Animator which is a copy of the Liftout Animator. These are all described above.

![Screenshot: Postwelder](/doc_screenshots/doc_postwelder_1.jpg?raw=true "Postwelder 1")

- The only new interface is the Post Simulator, which can be used to move the half-grid post in X,Y,Z,T and R. Finally, __Zero Post__ sets all post values to 0.

### Stage Simulator Window:

- Clicking the __Change to Stage Simulator__ button in the Liftout animator
  will bring you to the Stage Simulator:

![Screenshot: StageSim](/doc_screenshots/doc_stagesim_1.jpg?raw=true "StageSim 1")

This model is meant as an aid to navigating the stage in 3D, especially in newer triple-beam systems where hard-to-image-with beams like a laser need to be aligned. A pre-tilted stub with 54 and 36 degree surfaces can be moved using 5-axis controls that should closely mirror those of most FIB systems. 

(Note 04/08/2021: The stub didn't get updated to the 54 and 36 degree one for M&M, and is an older prototype with 45 and 60 degree surfaces. This will be fixed in an upcoming update. -A)

The eucentric height is set to 0 in this space, and coincidence for all beams is at (0,0,0). Controls for the Stage Simulator panel are:

<img align="left" width="250" src="/doc_screenshots/doc_stagesim_2.jpg">

- __Stage X/Y/Z/R/T:__ Common control axes for FIB stages. To move the stage click and drag horizontally to change values, or use the keyboard to enter specific values.
- __Zero Stage:__ Set all axes to 0
- __Go to viewpoint (e/i/laser):__ Show the (orthographic) view for each beam. Current angles between beams are 52 degrees between electron and ion beams, and 60 degrees between electron and laser beams.
- __Change to Liftout Animator:__ Go back to the Liftout Animator.

## Uh oh, I messed something up:

VirtualFIB has been built on top of Blender, and by default tries to hide some of the underlying complexity, both in interface and capability. While some things are hidden, they can easily be brought back, and the full power of Blender is still available to you. But with great power comes great responsibility<sup>[citation needed](https://www.explainxkcd.com/wiki/index.php/285:_Wikipedian_Protester)</sup>, and if unfamiliar with Blender it is easy to change the model or UI in ways you didn't intend, and you may not always be able to `ctrl+Z` to safety.

Luckily, since VirtualFIB is created as an application template with a dedicated 'default' file, you can always restart Blender or open a new Liftout Animator file, which should reload and go back to where you were. You can freely save your file, and as long as you don't overwrite the bundled *startup.blend* file Blender will reload to a known state.

If you had made changes to your saved file, but messed up the UI in the progress, you can restart Blender to get a new Liftout Animator file, then reload your own file, and in the loading menu click the cogwheel and disable `Load UI`, which should load in your revised file without doing changes to the UI itself.

## How to contribute

To change stuff and update the template, the whole repository can be cloned and worked with directly in the Blender Application Template folder, restarting Blender after changes to check every thing is working. However, the correct folder varies from system to system and will not be created before an application template is installed. Therefore, to make any changes, the easiest way to get up to speed is the following:

1. Install and check LA is working as explained above (Blender automatically creates the right folders in the right places).

2. Navigate to the liftout-animator application template folder. The precise location varies with your system and is detailed [here](https://docs.blender.org/manual/en/latest/advanced/app_templates.html) in the Blender documentation. On Windows, it should be *__User name__/AppData/Roaming/Blender Foundation/Blender/__Blender version__/scripts/startup/bl_app_templates_user*.

3. Close Blender if you have it open, and delete the liftout-animator folder. Now you can clone the repository to *bl_app_templates_user* and the next time you open blender it should automatically detect the template.

### Useful links

 - [On blender's application templates](https://docs.blender.org/manual/en/latest/advanced/app_templates.html)
 - [Where the application template can be found on your system](https://docs.blender.org/manual/en/latest/advanced/blender_directory_layout.html#blender-directory-layout)
 - [Blender Add-on tutorial](https://docs.blender.org/manual/en/latest/advanced/app_templates.html)
 - [HDRI Haven for HDRI maps](https://hdrihaven.com/)


