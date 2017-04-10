#!/usr/bin/env python

from ast import literal_eval
import os
from random import shuffle
from subprocess import Popen, PIPE

print 'Starting: {}'.format(__file__)

ignored_files = [
    'change-bg',
    'change-bg.py',
    'log.out',
    'log.err'
]

wallpapers = [
    x for x in
        os.listdir(os.path.expanduser('~/Pictures/wallpaper'))
        if x not in ['change-bg', 'log.out', 'log.err'] and
           not x.endswith('.py') and
           not x.endswith('.swp')
]

print 'Found wallpapers: {}'.format(wallpapers)

shuffle(wallpapers)

print 'Shuffled wallpapers: {}'.format(wallpapers)

def get_uri(image):
    return 'file://' + os.path.expanduser('~/Pictures/wallpaper/') + image

it = iter(wallpapers)
uri = get_uri(next(it))
print 'Using uri: {}'.format(uri)

print 'Checking current wallpaper...'
# If our current image matches the new one we just shuffled and picked,
# then we'll try the next image in the iterator.
p = Popen(
    ['gsettings', 'get', 'org.gnome.desktop.background', 'picture-uri'],
    stdout=PIPE
)
p.wait()
current_uri = literal_eval(p.stdout.read())
print 'Current wallpaper is: {}'.format(current_uri)
if current_uri == uri:
    uri = get_uri(next(it))
    print 'Using next wallpaper: {}'.format(uri)

# Set the new wallpaper
print 'Seting the wallpaper ...'
p = Popen(
    ['gsettings', 'set', 'org.gnome.desktop.background', 'picture-uri', uri],
    stdout=PIPE,
    stderr=PIPE
)
status = p.wait()
print 'gsettings stdout: {}'.format(p.stdout.read())
print 'gsettings stderr: {}'.format(p.stderr.read())
if status != 0:
    print 'Setting wallpaper failed with status {}'.format(status)
else:
    print 'Setting wallpaper succeeded!'
