window.DASHBOARD_DATA = {
  "generated_at": "2026-03-16 22:51:51",
  "jobs": [
    {
      "name": "Backup to Q (rsync)",
      "schedule": "Daily 12:00",
      "hour": 12,
      "last_run": "2026-03-16 22:36:55",
      "status": "warning",
      "progress": 22,
      "steps": [
        {
          "name": "tryhackme",
          "status": "ok"
        },
        {
          "name": "monochrome",
          "status": "warning"
        },
        {
          "name": "mcloud_download",
          "status": "pending"
        },
        {
          "name": "mcloud_playlists",
          "status": "pending"
        },
        {
          "name": "shazams",
          "status": "pending"
        },
        {
          "name": "language-study",
          "status": "pending"
        },
        {
          "name": "dabmusic",
          "status": "pending"
        },
        {
          "name": "daily",
          "status": "pending"
        },
        {
          "name": "snowflake_data_engineering(coursera)",
          "status": "pending"
        }
      ],
      "counts": {
        "Folders synced": 2,
        "Folders skipped": 0,
        "Rsync errors": 1
      },
      "log_tail": [
        "deleting imdb_episode_search.py",
        "deleting everything_export.csv",
        "deleting episode_search.py",
        "deleting episode_search.ipynb",
        "deleting embyserver.txt",
        "deleting correct_library.ipynb",
        "deleting copy_emby_db.py",
        "deleting copy_books_to_reader.ipynb",
        "deleting alldebrid_list_links.ipynb",
        "deleting Cookies"
      ],
      "next_run": "2026-03-17 12:00:00"
    },
    {
      "name": "Import Spotify",
      "schedule": "Daily 13:00",
      "hour": 13,
      "last_run": null,
      "status": "no_log",
      "progress": 0,
      "steps": [],
      "counts": {},
      "log_tail": [],
      "next_run": "2026-03-17 13:00:00"
    },
    {
      "name": "Sync KCRW",
      "schedule": "Daily 14:00",
      "hour": 14,
      "last_run": "2026-03-16 22:51:49",
      "status": "ok",
      "progress": 100,
      "steps": [],
      "counts": {
        "Tracks synced (total)": 3346
      },
      "log_tail": [
        "2026-03-16 22:51:38,438 INFO   + Sophie May - Another Song for the End of the World [364989006]",
        "2026-03-16 22:51:38,438 INFO   + Sophie May - Another Song for the End of the World [364989006]",
        "2026-03-16 22:51:40,591 INFO   + Hohnen Ford - Infinity [194595564]",
        "2026-03-16 22:51:40,591 INFO   + Hohnen Ford - Infinity [194595564]",
        "2026-03-16 22:51:43,761 INFO   + Coldplay - Spies [35533516]",
        "2026-03-16 22:51:43,761 INFO   + Coldplay - Spies [35533516]",
        "2026-03-16 22:51:46,636 INFO   + Crazy P - Heartbreaker [5715593]",
        "2026-03-16 22:51:46,636 INFO   + Crazy P - Heartbreaker [5715593]",
        "2026-03-16 22:51:49,702 INFO   + Fred again.. - Talk of the Town [366631881]",
        "2026-03-16 22:51:49,702 INFO   + Fred again.. - Talk of the Town [366631881]"
      ],
      "next_run": "2026-03-17 14:00:00"
    },
    {
      "name": "Run KCRW Daily",
      "schedule": "Daily 14:00",
      "hour": 14,
      "last_run": "2026-03-16 17:27:20",
      "status": "error",
      "progress": 85,
      "steps": [
        {
          "name": "import_kcrw.py",
          "status": "ok"
        },
        {
          "name": "kcrw_dedup.py",
          "status": "ok"
        },
        {
          "name": "kcrw_monochrome_import.py",
          "status": "error"
        },
        {
          "name": "local_kcrw_import.py",
          "status": "ok"
        },
        {
          "name": "soundcloud_search.py",
          "status": "ok"
        },
        {
          "name": "download_soundcloud_errors.py",
          "status": "error"
        }
      ],
      "counts": {
        "Scripts OK": 4,
        "Scripts failed": 2
      },
      "log_tail": [
        "[download]  91.0% of ~   1.70MiB at  456.59KiB/s ETA 00:01 (frag 21/22)",
        "[download]  96.7% of ~   1.60MiB at  461.43KiB/s ETA 00:01 (frag 21/22)",
        "[download]  96.8% of ~   1.60MiB at  461.43KiB/s ETA 00:01 (frag 21/22)",
        "[download]  96.9% of ~   1.60MiB at  461.43KiB/s ETA 00:01 (frag 21/22)",
        "[download]  97.1% of ~   1.60MiB at  461.43KiB/s ETA 00:01 (frag 21/22)",
        "[download]  97.6% of ~   1.61MiB at  461.43KiB/s ETA 00:01 (frag 21/22)",
        "[download]  98.1% of ~   1.63MiB at  461.43KiB/s ETA 00:01 (frag 21/22)",
        "[download]  96.7% of ~   1.65MiB at  461.43KiB/s ETA 00:01 (frag 22/22)",
        "[download] 100% of    1.60MiB in 00:00:03 at 428.93KiB/s               ",
        "[ExtractAudio] Destination: /home/malston/q/Music/YouTube_Music7/KCRW (Error)/2026-03-13/Empire of the Sun - walking on a dream.mp3"
      ],
      "next_run": "2026-03-17 14:00:00"
    },
    {
      "name": "Update TryHackMe Vocab",
      "schedule": "Daily 15:00",
      "hour": 15,
      "last_run": null,
      "status": "no_log",
      "progress": 0,
      "steps": [],
      "counts": {},
      "log_tail": [],
      "next_run": "2026-03-17 15:00:00"
    }
  ]
};
