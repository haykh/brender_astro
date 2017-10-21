Installation for Mac users
**************************************

Installation
================================

Clone BRender repo
----------------------------
1. Go to any desired directory of your choice.
2. Do ``$ git clone https://github.com/haykh/brender_astro.git`` to clone the repo.
3. The library and all the necessary files will be downloaded to the current directory.

.. warning::

    We'll next download and install the main Blender app. This requires several hundreds MB of disk space, so be prepared.

Installing and configuring Blender
--------------------------------------------------------
1. Download Blender app from `here <https://www.blender.org/download/>`_.
2. Drag and drop Blender app to the Applications folder.

.. note::

    We then need to adjust some of the Blender import/export files. You can do it manually following steps 3-6, or if you have version 2.79 you can simply download the already fixed files and replace the original ones (see step 7).

3. Navigate to the following folder::

    $ cd /Applications/blender.app/Contents/Resources/2.**/scripts/addons/io_scene_obj/

where ``2.**`` is your Blender version, which in my case is ``2.79``.


4. Open ``import_obj.py`` and add these two lines:

.. code-block:: python
    :emphasize-lines: 5,6

    # ...
    elif line_id == b'tf':
        # rgb, filter color, blender has no support for this.
        pass
    elif line_id == b'em': # ADD THIS LINE (BRender)
        context_material.emit = float_func(line_split[1]) # ADD THIS LINE (BRender)
    elif line_id == b'illum':
        illum = int(line_split[1])
    # ...


5. In the same file comment out the following line:

.. code-block:: python
    :emphasize-lines: 7

    # ...
    if emit_value > 1e-6:
        if use_cycles:
            print("WARNING, currently unsupported emit value, skipped.")
        # We have to adapt it to diffuse color too...
        emit_value /= sum(context_material.diffuse_color) / 3.0
    # context_material.emit = emit_value # <- COMMENT THIS LINE OUT (BRender)
    if not do_ambient:
    	context_material.ambient = 0.0
    # ...

6. Save the file and open ``export_obj.py``. Add this line and save the file:

.. code-block:: python
    :emphasize-lines: 6

    # ...
    	elif mat.use_transparency and mat.transparency_method == 'RAYTRACE':
    		fw('illum 9\n')  # 'Glass' transparency and no Ray trace reflection... fuzzy matching, but...
    	else:
    		fw('illum 2\n')  # light normaly
    	fw('em %.6f\n' % mat.emit) # ADD THIS LINE (BRender)
    else:
        # Write a dummy material here?
    # ...

7. For the sake of convenience, I `added <https://github.com/haykh/brender_astro/tree/master/blender_files/2.79_Mac>`_ those two ``.py`` files for Blender 2.79, so you can just download and replace the original ones which are in here ``/Applications/blender.app/Contents/Resources/2.79/scripts/addons/io_scene_obj/``.

Configuring Blender's bundled python
--------------------------------------------------------
- For Blender version 2.79 (on Mac) do::

	$ bash setup_python.sh

from the ``setup_python/`` directory (where the ``get-pip.py`` file is). This will install ``pip`` using the ``get-pip.py`` file (from the same directory as the ``.sh`` file) in the bundled python and will then install ``h5py`` which is necessary for loading ``hdf5`` files in the Blender.

- For newer/older versions you can try adjusting the directory in the ``.sh`` file, but since the python version can change, this might not work. Anyway, in general the idea is to have Blender's bundled python run the ``get-pip.py`` file (to install ``pip``), and then run the newly installed Blender's bundled pip to install ``h5py``. Something like this::

	$ /path/to/blender.app/Contents/Resources/2.XX/python/bin/python get-pip.py
	$ /path/to/blender.app/Contents/Resources/2.XX/python/bin/pip install h5py


Blender setup
====================================

1. If you haven't cloned this repo yet, it's time to do it::

    $ cd /any-folder-you-like/
    $ git clone https://github.com/haykh/brender_astro.git

2. Then navigate to ``initialize_blender/`` inside the cloned repository and open ``init_script.py``.
3. Modify the path in the 2-nd line writing the correct path to the downloaded BRender repo.
4. Open ``bash_profile`` with ``$ open -e ~/.bash_profile`` and add the following line with a correct path to the downloaded repo::

    alias blender='/Applications/blender.app/Contents/MacOS/blender -P /path/to/brender/initialize_blender/init_script.py'

5. Restart the terminal. Now if we do ``$ blender`` in the terminal, the Blender app will launch pre-running the ``init_script.py``, which imports the module and does a quick setup of lighting.

6. From cloned BRender repo copy ``initialize_blender/mac/startup.blend`` file to ``/Users/<user>/Library/Application Support/Blender/2.**/config`` (if the folder doesn't exist - create it). This will set a default working screen that (for me) fits the best for script-based visualization.

Now once you run::

    $ blender

from the terminal, you should see two Blender windows (especially convenient if you use two screens).

.. figure::  /images/img_1.png
   :align:   center

- (*left*) code editor in case we want to run or edit a large script
- (*right*) python console that uses Blender's bundled Python 3 (most of the time we'll be using this console)
- (*down*) code editor log


.. figure::  /images/img_2.png
   :align:   center

- (*left*) 3D viewport with all the objects of our scene
- (*middle*) rendered image will be displayed here, which is now just empty
- (*right*) ``Properties`` tab with all the material and object properties

7. You can also configure your own workspace layout (consoles, 3d viewports etc) and save it as default by doing ``Ctrl+U``.
