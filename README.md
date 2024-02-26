# hass_remove_devices

Very simple python script to remove dead devices and entities from Home
Assistant

Use at your own risk!

Steps:

1. Rename devices to add " dead" in the name at the end
2. Put the script in the HA home directory (where the .storage directory is
   located)
3. Stop HA (depends on how you run it)
4. Run using python (you may need sudo)
4. The script will create two .bak files and two .upd files. The script operates
   on core.device_registry and core.entity_registry files. Files are not
   modified by the script, instead .upd files are created
6. You may use diff to see the difference
7. Copy .upd files to replace original files
8. Start HA
