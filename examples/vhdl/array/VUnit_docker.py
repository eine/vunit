from os.path import basename, dirname, realpath, abspath, isfile
from os import environ, pathsep
import sys, docker

from colorama import Fore

class VUnit():

    def from_argv(argv=sys.argv, vols={}):
        from argparse import ArgumentParser
        p = ArgumentParser(description='Dockerized VUnit')
        p.add_argument('-d', '--docker', action="store_true", dest="dockervar")
        args, uargs = p.parse_known_args(argv)

        if args.dockervar is True:
            VUnit(uargs, vols=vols).run()
            exit(0)
        else:
            try:
                import vunit
            except:
                sys.path.insert(0, '/work/vunit')
                try:
                    import vunit
                except:
                    print('Error. Could not import VUnit. Please, set VUNIT_DIR')
                    exit(1)

            environ['PATH'] += pathsep + abspath(realpath(dirname(vunit.__file__)+"/../bin"))
            ui = vunit.VUnit.from_argv()
            return ui

    def __init__(self, argv, vols={}):

        print(Fore.CYAN + '[Dockerized VUnit] ', end='')
        print(Fore.WHITE + 'Init VUnit object')

        self.client = docker.from_env()
        self.sim_img = 'ghdl/ghdl:ubuntu18-llvm-5.0'
        self.run_img = 'vunit/run:3.6-alpine'
        self.vols = vols
        self.args = [basename(argv[0])] + argv[1:]

        # get/set Sim image
        sim_img = environ.get('VUNIT_SIM_IMG')
        if sim_img is not None:
            self.sim_img = sim_img

        # get/set Run image
        run_img = environ.get('VUNIT_RUN_IMG')
        if run_img is not None:
            self.run_img = run_img

        # get Run dir
        run_dir = environ.get('VUNIT_RUN_DIR')
        if run_dir is None:
            runpy = abspath(realpath(argv[0]))
            if isfile(runpy) is True:
                run_dir = dirname(runpy)
            else:
                print('Error. Could not get the Sources path. Please, set VUNIT_RUN_DIR')
                exit(1)
        self.vols[run_dir] = {'bind': '/work/run', 'mode': 'rw'}

        # get VUnit dir
        try:
            import vunit
            vunit_dir = abspath(realpath(vunit.__file__))
        except:
            vunit_dir = environ.get('VUNIT_DIR')
            if vunit_dir is None:
                print('Error. Could not get the VUnit path. Please, set VUNIT_DIR')
                exit(1)
        self.vols[vunit_dir] = {'bind': '/work/vunit', 'mode': 'ro'}

    def run(self):

        print(Fore.CYAN + '[Dockerized VUnit] ', end='')
        print(Fore.WHITE + 'Start containers in the background')

        # (re)start sim container in the background
        try:
            container = self.client.containers.get('vunit-sim')
            container.remove(force=True)
        except:
            pass
        try:
            container = self.client.containers.run(
                image=self.sim_img,
                name='vunit-sim',
                detach=True,
                volumes=self.vols,
                command=['tail','-f','/dev/null']
            )
        except Exception as inst:
            print(inst)
            exit(1)
        print('vunit-sim: ', container.short_id, container.status, container.image.tags)

        # (re)start run container in the background
        try:
            container = self.client.containers.get('vunit-run')
            container.remove(force=True)
        except:
            pass
        try:
            container = self.client.containers.run(
                image=self.run_img,
                name='vunit-run',
                detach=True,
                volumes={'/var/run/docker.sock':{'bind':'/var/run/docker.sock','mode':'rw'}},
                volumes_from=['vunit-sim'],
                command=['tail','-f','/dev/null']
            )
        except Exception as inst:
            print(inst)
            exit(1)
        print('vunit-run: ', container.short_id, container.status, container.image.tags)

        print(Fore.CYAN + '[Dockerized VUnit] ', end='')
        print(Fore.WHITE + 'Execute python run script in the foreground')

        def remove_containers():
            print(Fore.CYAN + '[Dockerized VUnit] ', end='')
            print(Fore.WHITE + 'Remove containers')
            self.client.containers.get('vunit-run').remove(force=True)
            self.client.containers.get('vunit-sim').remove(force=True)

        # execute python run script in the foreground
        try:
            print(container.exec_run(
                ['python'] + self.args,
                workdir='/work/run'
            ).output.decode('UTF-8'))
        except Exception as inst:
            # TODO: extract the content from the Error object and decode it with .decode('UTF-8')
            print(inst)
            remove_containers()
            exit(1)
        remove_containers()
