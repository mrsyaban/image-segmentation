<div align="center">
  <h1 align="center">Semantic Segmentation</h1>

  <p align="center">
    *R-CNN Semantic Segmentation* Optimization using Divide-and-Conquer Algorithm
    <br />
    <a href="http://bit.ly/ImageSegmentationDemo">View Demo    </a>
    ·
    <a href="https://github.com/mrsyaban/image-segmentation">    Explore the docs</a>
  </p>
</div>


<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>


## About The Project
Suatu citra dapat diolah menjadi sumber informasi jika diolah dengan Teknik tertentu. Salah satu bagian penting untuk memperoleh informasi yang lebih terperinci tentang objek atau struktur di dalam citra adalah dengan memisahkan piksel-piksel yang saling terkait menjadi kelompok-kelompok yang koheren dan bermakna. Salah satu Teknik pemisahan objek dari citra adalah dengan algoritma Regional Convolution Neural Network (R-CNN), namun algoritma ini tidak efektif di semua kasus. Penggunaan algoritma yang tepat dapat mengoptimasi segmentasi gambar agar dapat lebih akurat. Salah satu algoritma yang dapat digunakan adalah Algoritma Divide and Conquer (DnC) yang membagi gambar menjadi beberapa wilayah lalu melakukan segmentasi terpisah pada masing-masing wilayah yang kemudian disatukan kembali menjadi segmentasi gambar yang utuh. Didapatkan bahwa algoritma DnC dapat mengoptimalisasi proses segmentasi pada gambar-gambar dengan jumlah objek yang besar


### Built With
    - PyQt5 v5.15.9
    - numpy v1.23.5
    - opencv-python v4.6.0.66
    - matplotlib v3.5.0
## Getting Started

### Prerequisite
install all tect stack 

  ```sh
  pip install PyQt5@5.15.9 numpy@1.23.5 opencv-python@4.6.0.66 matplotlib@3.5.0
  ```

### Installation
1. Clone this repo
   ```sh
   git clone https://github.com/mrsyaban/image-segmentation
   ```
2. ketik `python src/main.py` pada directory repo ini
    ```sh
   python src/main.py
   ```

## Usage
1. klik `Choose Image` button in the bottom of the window to choose image that you want
2. you can choose image from `test/`
3. just wait and boom!

<p align="center">
    <img src="https://github.com/mrsyaban/image-segmentation/blob/main/doc/lampiran.png" width="600">
</p>

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.


## Authors

| NIM      | NAMA                        |
|----------|-----------------------------|
| 13521119 | Muhammad Rizky Sya’ban      |

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments
Terima kasih kepada bapak Dr. Ir. Rinaldi, M.T. dan seluruh tim pengajar IF2211 Strategi Algoritma yang telah memberikan penulis kesempatan dalam pembuatan makalah ini dan juga saya ingin berterim kasih kepada Girshick, dkk. yang telah menemukan algoritma RCNN. 