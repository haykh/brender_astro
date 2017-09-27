# __BRender__
## Python-based data visualization module for Blender
### _Designed for TRISTAN p-i-c code output_

> Some of the features are borrowed from [AstroBlend](http://www.astroblend.com/).

## Step-by-step guide (OS X)

### Installing and configuring Blender
1. Download Blender app from [here](https://www.blender.org/download/).
2. Drag and drop Blender app to the Applications folder.
3. Navigate to the following folder (`2.**` is your Blender version, which in my case is `2.79`):

	```sh
	$ cd /Applications/blender.app/Contents/Resources/2.**/scripts/addons/io_scene_obj/
	```
4. Open `import_obj.py` and add these two lines:

	```python
	# ...
	elif line_id == b'tf':
	    # rgb, filter color, blender has no support for this.
	    pass
    elif line_id == b'em': # ADD THIS LINE (BRender)
	    context_material.emit = float_func(line_split[1]) # ADD THIS LINE (BRender)
	elif line_id == b'illum':
	    illum = int(line_split[1])
    # ...
	```
6. In the same file comment out the following line:

	```python
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
	```
6. Save the file and open `export_obj.py`. Add this line and save the file:

	```python
	# ...
		elif mat.use_transparency and mat.transparency_method == 'RAYTRACE':
			fw('illum 9\n')  # 'Glass' transparency and no Ray trace reflection... fuzzy matching, but...
		else:
			fw('illum 2\n')  # light normaly
		fw('em %.6f\n' % mat.emit) # ADD THIS LINE (BRender)
	else:
	    # Write a dummy material here?
    # ...
	```
7. Just in case I added two of those `.py` files [here](https://github.com/haykh/brender_astro/tree/master/blender_files), so you can just download and replace original ones (for Blender 2.79).
