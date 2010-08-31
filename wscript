import sys
import Options
from os import unlink, link
from os.path import exists 

# nice, but requires python 2.6 ... 
#import json
#package = json.load(open('package.json'))
#APPNAME = 'node_' + package['name'] # used by 'node-waf dist'
#VERSION = package['version']        # dito

APPNAME = 'node_mdns'
VERSION = '0.0.3'

def set_options(opt):
  opt.tool_options('compiler_cxx')

def configure(conf):
  conf.check_tool('compiler_cxx')
  conf.check_tool('node_addon')
  if sys.platform != 'darwin':
    conf.env.LIB_DNSSD = 'dns_sd'
  conf.check(
    function_name='DNSServiceGetAddrInfo',
    header_name="dns_sd.h",
    define_name='HAVE_GET_ADDR_INFO',
    mandatory=0)
  conf.write_config_header('node_mdns_config.h');

def build(bld):
  obj = bld.new_task_gen('cxx', 'shlib', 'node_addon')
  obj.target = 'binding'
  obj.source = bld.path.ant_glob('src/*.cpp')
  obj.uselib = "DNSSD"
  obj.includes = '.'
                

def shutdown():
  # HACK to get binding.node out of build directory.
  # better way to do this?
  if exists('lib/binding.node'): unlink('lib/binding.node')
  if Options.commands['build']:
    link('build/default/binding.node', 'lib/binding.node')

# vim: set filetype=python :
