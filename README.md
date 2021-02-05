# liftout-animator
Blender application template to animate in-situ liftout.

## How to run

Liftout-Animator (LA) builds on the Open-Source software Blender, which provides the toolbox to do 3D operations and full freedom to change anything. To install LA we first need to install blender:

1. Download and install [Blender](https://www.blender.org/download/). This version was last tested on Blender version 2.91.2 (but should be stable for future minor revisions).

2. Download .zip of LA code from this repository.

3. Install and run Blender, then click the blender icon in the top left toolbar and select Install Application Template

4. Select the downloaded .zip and install. Restart Blender and on the splashscreen select __Liftout Animator__. Alternatively, in an open Blender window, select `File>New>Liftout Animator`

## Usage

After install, when you now open Blender the Splash screen should have a `...` field where you can select Liftout Animator.

![](/doc_screenshots/doc_splash1.jpg?raw=true "Splash screen")

Alternatively, press `ctrl+n` for a new file and select Liftout Animator. This will load the default LOA file and control window.



The 

## Developer Guide

To change stuff and update the template, the whole repository can be cloned and worked with directly in the Blender Application Template folder, restarting Blender after changes to check every thing is working. However, the correct folder varies from system to system and will not be created before an application template is installed. Therefore, to make any changes, the easiest way to get up to speed is the following:

1. Install and check LA is working as explained above (Blender automatically creates the right folders in the right places).

2. Navigate to the liftout-animator application template folder. The precise location varies with your system and is detailed [here](https://docs.blender.org/manual/en/latest/advanced/app_templates.html) in the Blender documentation. On Windows, it should be **Username**/AppData/Roaming/Blender Foundation/Blender/**Blender version**/scripts/startup/bl_app_templates_user.

3. Close Blender if you have it open, and delete the liftout-animator folder. Now you can clone the repository to bl_app_templates_user and the next time you open blender it should automatically detect the template.

### Useful links

 - [On blender's application templates](https://docs.blender.org/manual/en/latest/advanced/app_templates.html)
 - [Where the application template can be found on your system](https://docs.blender.org/manual/en/latest/advanced/blender_directory_layout.html#blender-directory-layout)
 - [Blender Add-on tutorial](https://docs.blender.org/manual/en/latest/advanced/app_templates.html)
 - [HDRI Haven for HDRI maps](https://hdrihaven.com/)


