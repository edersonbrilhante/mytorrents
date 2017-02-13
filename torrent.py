import libtorrent as lt
import time
import logging
import shutil

log = logging.getLogger(__name__)


class Torrent(object):

    def start(self, name, subtitle_file, new_subtitle_file):
        ses = lt.session()
        ses.listen_on(6881, 6891)

        # e = lt.bdecode(open(name, 'rb').read())
        info = lt.torrent_info(name)
        params = {
            'save_path': './series/',
            'storage_mode': lt.storage_mode_t.storage_mode_sparse,
            'ti': info
        }
        h = ses.add_torrent(params)
        s = h.status()
        while (not s.is_seeding):
            s = h.status()

            state_str = ['queued', 'checking', 'downloading metadata',
                         'downloading', 'finished', 'seeding', 'allocating',
                         'checking_resume_data']
            print('Serie %s - %.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s' % (
                (h.name(), s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000,
                 s.num_peers, state_str[s.state])))

            time.sleep(10)
        try:
            shutil.move(subtitle_file, '/vagrant/series/{}/{}'.format(h.name(), new_subtitle_file))
        except:
            pass
