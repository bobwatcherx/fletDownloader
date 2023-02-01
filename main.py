import os
import requests
import time
from tqdm import tqdm
from flet import *

# Create the downloads folder if it does not exist
downloads_folder = "downloads"
if not os.path.exists(downloads_folder):
    os.makedirs(downloads_folder)




def main(page:Page):

    listdownload = GridView(
        expand=1,
        runs_count=5,
        max_extent=150,
        child_aspect_ratio=1.0,
        spacing=5,
        run_spacing=5,
        )
    folder_path = 'downloads'
    files_in_folder = os.listdir(folder_path)

    for file in files_in_folder:
        listdownload.controls.append(
            Column([
                Icon(name="photo_library",color="blue",size=60),
                Text(file,size=20)
                ])

            )

    # DOWNLOAD 
    def download(txturl, resultfile, start=0):
        progress_file = os.path.join(downloads_folder, resultfile + '.progress')
        save_path = os.path.join(downloads_folder, resultfile)
        if os.path.exists(progress_file):
            with open(progress_file, 'r') as f:
                start = int(f.read())
        headers = {"Range": f"bytes={start}-"}
        response = requests.get(txturl, headers=headers, stream=True)
        total_size = int(response.headers.get("Content-Length", 0)) + start
        progress = tqdm(response.iter_content(1024), f"Downloading {resultfile}", total=total_size, unit="B", unit_scale=True, unit_divisor=1024, bar_format="{percentage:.0f}%|{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]", initial=start)
        with open(save_path, "ab") as f:
            print("YOU FILE IS DOWNLOADING ......")
            page.splash = ProgressBar()
            page.snack_bar = SnackBar(
                Text("PleaseWait Downlaoding",size=20,color="white"),
                bgcolor="green"
                )
            page.snack_bar.open = True
            page.update()
            for data in progress:
                f.write(data)
                progress.update(len(data))
                print(progress)
                with open(progress_file, 'w') as pf:
                    pf.write(str(progress.n))
        end = time.time()
        elapsed = end - start
        if elapsed :
            print("sudah selesai ")
            page.splash = None
            page.snack_bar = SnackBar(
                Text("FInish downloading..",size=20,color="white"),
                bgcolor="blue"
                )
            page.snack_bar.open = True
            listdownload.controls.clear()
            for file in files_in_folder:
                listdownload.controls.append(
                    Column([
                Icon(name="photo_library",color="blue",size=60),
                Text(file,size=20)
                ])

                    )
                listdownload.update()

            page.update()
            print(f"Download completed in {int(elapsed)} seconds.")
        page.update()

    txturl = TextField(label="add Url")
    resultfile = TextField(label="you result file name")

    page.add(
        AppBar(
            bgcolor="blue",
            title=Text("Download manager example",
                color="white",
            size=20,weight="bold"),
        ),
        Column([
        txturl,
        resultfile,
        ElevatedButton("Download Now",
            bgcolor="blue",
            color="white",
            on_click=lambda e:download(txturl.value,resultfile.value,
            )
        ),
        Divider(),
        Text("You Download result",size=20,weight="bold"),
        # ALL DOWNLOAD
        Row([
            listdownload
            ],alignment="center")

            ])
        )

flet.app(target=main)
