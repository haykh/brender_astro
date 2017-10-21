**************
Volume plot
**************

Before starting this section make sure to have a camera set up. Also if there's a bounding box in the scene, it's generally easier to navigate and understand the directions in space. So before moving forward, check :ref:`previous tutorial <brbasics>` on basics of BRender.

.. note::

    `for tigressdata users`. Blender's bundled python does not support ``hdf5`` documents, and I wasn't able to install it (no access). So you'll have to do all the reading and primary analysis of all the data from some python outside Blender.


Generating VOXEL data
=======================

In general BRender is not constrained to any specific code output, and can be fed by any sort of Blender VOXEL (volumetric pixel) data file generated in advance. So if you know how to generate a ``.bvox`` file from a specific code output, feel free to skip to the next section where we'll be making a volumetric plot.

Here we'll discuss how to generate a ``.bvox`` file particularly for TRISTAN code output (``hdf5`` format), which will be later used to make a plot. Note again, that if you're working from within the tigressdata, you'll have to do this from a python outside Blender, Mac users can do this from inside Blender console. We first need to specify several paths and names::

    # For tigressdata do this whole procedure from outside Blender python console
    out_path = '/output-dir-for-bvox/' # <-- make sure to have slash in the end
    fname = '/path-to/flds.tot.001' # <-- this one is specifically a TRISTAN output file
    prefix = 'density' # <-- this is the prefix name of the file, in our case - density

Let's say we want to plot a density. For that we specify a value function which takes the code data as an input and outputs the desired field in the correct form::

    def valueFunc(data):
        return data['dens'].value # <-- we output whatever is under 'dens' key value

.. note::

    If you don't specify ``valueFunc()`` it will take a default function (which is just the ``'dens'`` key).

.. note::

    You could think of something more complicated, like a current density normalized by the distance to the center of the grid squared (this is relevant to pulsar magnetosphere simulations)::

        def valueFunc(data):
            sx, sy, sz = data['jx'].value.shape
            halfx, halfy, halfz = map(np.floor, np.array([sx, sy, sz]*0.5))
            rsquared = np.array([[[((x - halfx)**2 + (y - halfy)**2 + (z - halfz)**2) for x in range(sx)] for y in range(sy)] for z in range(sz)])
            return np.sqrt(np.array(data['jx'].value)**2 + np.array(data['jy'].value)**2 + np.array(data['jz'].value)**2) * rsquared

We can also specify a normalization function if we want (the default is just linear normalization)::

    def normalizeFunc(value):
        return np.log(1. + value) # <-- accepts real value and outputs normalized value

Other two options to specify are the maximum and minimum value. After the normalization, any value in the 3D grid above that maximum value and below the minimum will be diminished and set to the specified value::

    min_val = 0.1 # <-- our function does the following val[val < min_val] = min_val
    max_val = 0.8 # <-- our function does the following val[val > max_val] = max_val

.. note::

    Default (in case you don't specify) for ``min_val`` is 0, and for ``max_val`` is 1.

Ok, now with all those variables and functions specified, we are ready to output a ``.bvox`` file in the directory specified above::

    import lib.to_bvox as bvox
    bvoxfile = bvox.makeBvox(out_path, fname,
                                valueFunc = valueFunc,                      # optional
                                normalizeFunc = normalizeFunc,              # optional
                                min_val = min_val, max_val = max_val,       # optional
                                prefix = prefix)                            # optional
    # now bvoxfile is a string containing the path to the generated `.bvox` file in case you need it

.. warning::

    For tigressdata you'll first need to append ``sys.path`` when working outside Blender (add this at the start of code)::

        import sys
        sys.path.append('/path-to-BRender-repo/') # you can use mine '/home/hakobyan/Downloads/brender_astro'

    Also make sure you have ``h5py`` module loaded (in the terminal)::

        $ module load h5py27

Making volumetric plot
========================

Finding the shape and scale
------------------------------

Since you'll later need a shape of your simulation and scaling factor for your visualization, I'd suggest to do it right away with the following code::

    # make sure to do 'import lib.to_bvox as bvox' as you probably did above
    fname = '/path-to/flds.tot.001'
    shape0 = np.array(bvox.getShape(fname, 'dens'))
    scale = 1 / (2.* shape0.min())
    shape = shape0 * scale

Now ``shape`` is a tuple of 3 float numbers with the normalized ``(size-x, size-y, size-z)`` of your data, and ``scale`` is a float number that determines how much is the original data "squeezed". Again, tigressdata users can run this only outside Blender's python.

Nailing the plot
------------------------------

.. note::

    For tigressdata the rest can be done within the Blender console.

If you working within tigressdata, specify a path to ``.bvox`` file::

    bvoxfile = '/home/hakobyan/Downloads/outputs/bvox/dens.bvox'

You then can make an object that will have your volumetric plot::

    density = br.VolumePlot(bvoxfile, name = 'my_density')

This creates a cube and fills it in according to voxel data. You can then work with this ``density`` object. By default the density is in 2x2x2 cube. We can adjust it by doing::

    density.size = shape # <-- set the shape to already predefined

We can also adjust the colormap and brightness::

    # let us first define a colormap
    cmap = [[0.0, # <-- this is the position of the first color tag
                (0, 0, 1, 0)], # <-- this is the color in terms of (r, g, b, a)
            [0.7,
                (0, 0, 1, 0.3)],
            [0.86,
                (0.56, 0.878, 0.002, 0.8)],
            [1,
                (1, 0, 0, 1.0)]]
    # ... and brightness
    brightness = 0.6
    density.cmap = cmap
    density.brightness = brightness

Other more complex parameters to adjust are the ``density`` and ``contrast``::

    density.density = 5.
    density.contrast = 0.35

.. note::

    You can always play with those parameters (colormap, brightness, contrast, density, etc) from the Blender GUI (see below).

    .. figure::  /images/gif_5.gif
       :align:   center

Below is a rendering result of such a plot.

.. figure::  /images/img_5.png
   :align:   center

.. note::

    We can also enable the interactive viewport to look at the result from different angles on the fly (:ref:`see here <interactive>` on how to do this).
