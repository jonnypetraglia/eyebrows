# Eyebrows - Simple web file browser written in Python #
#### Copyright 2014 Jon Petraglia of Qweex ####
#### http://qweex.com ####

### Contents: ###
  1. Configuration
  2. Why
  3. Dependencies
  4. Licenses
  5. Misc Notes

------------------------------------------------------

1. Configuration
----------------

Dude I don't even know about config yet. So far here is what you can do:
  * baseFolder = the folder you want to start in and restrict access to
  * port = port it will be serving on
  * hideBarsDelay = for images how many ms before the titlebar hides; set to 0 for it to never hide
  * protocol = either "HTTP/1.0" or "HTTP/1.1"
  * useSSL = whether or not to serve through SSL; hint: do it
  * username = for authentication
  * password = for authentication
  * ignoreHidden = whether or not to ignore hidden files
  * useDots = if you want to use the traditional ".." to navigate to the parent directory instead of the up button
  * uploadEnabled = whether or not to allow the user to upload files

2. Why?
----------------

I've used some programs like Dropbox or Tonido, but I wanted similar access without the baggage of using a service.

So basically, I wanted a simple all-in-one server application to access my files from anywhere with good mobile and pictures support.

Also I wanted to write something simple in Python.


3. Dependencies
----------------

  * [Python 3.3.3](http://www.python.org/)
  * [Mako 0.9.1](http://www.makotemplates.org/)
  * [ZipStream 859532](https://github.com/allanlei/python-zipstream/tree/859532b05844a0eb3efd641303a08d4424edb30e)
  * [FineUploader 4.2](http://fineuploader.com/)
  * [jQuery 1.10.2](http://jquery.com/)
  * [Bootstrap 3.0.3](http://getbootstrap.com/)
  * [FontAwesome 4.0.3](http://fontawesome.io/)
  * [Swipebox 4e8338](https://github.com/brutaldesign/swipebox/tree/4e8338ec2740ca75eb8a39247c275f1a1b3d7539)
  * [Sala de Fiest font](http://openfontlibrary.org/en/font/sala-de-fiesta)
  * [Eyebrow Photoshop Brush](http://www.photoshopwebsite.com/photoshop-brushes/28-photoshop-eyebrow-brushes-free-download/)


Optional:
  * [pywin32 218](http://sourceforge.net/projects/pywin32/) (if you want to set "ignoreHidden" on Windows)

4. Licenses
----------------

All licenses can be found in the "licenses" directory

Eyebrows itself is released under the BSD license.

Other components are licensed as followed:
  * Python: PSF
  * Mako: MIT
  * ZipStream: GPLv3
  * FineUploader: GPLv3
  * jQuery: MIT
  * Bootstrap: MIT
  * FontAwesome: OFL & MIT
  * Swipebox: MIT
  * Sala de Fiesta: MIT:
  * Eyebrow Photoshop Brush: Custom
  * pywin32: PSF

5. Misc Notes
----------------

### Video ###

Eyebrows *technically* supports in-browser video. BUT it is not guaranteed to work and depends on the browser you are using.
Eyebrows does **NOT** use HTML5 *or* Flash for video playback, it simply embeds the video in the page and leaves it to your browser to use a plugin.

Why not either of the options I stated? Because (a) Support for video in HTML5 is unreliable across browsers and (b) Flash is a dying technology (aaaand I couldn't find an acceptible open-source flash playerm; key word: 'acceptible').

### Browser Support ###

Eyebrows *should* theoretically work with just about any browser out there.

*However*, it takes advantage of a lot things like CSS3 and HTML5 that might not work correctly in older browsers.