# PDF

## Table of Contents

- [PDF](#pdf)
  - [Table of Contents](#table-of-contents)
  - [OCR](#ocr)

## OCR

**Install necessary tools**
Update the package list and install Tesseract with support for the desired language. Replace `fra` with your desired language code (e.g., `eng` for English).

```bash
apt update
apt install tesseract-ocr tesseract-ocr-fra
```

**Verify the installation**

Check the installed version of Tesseract and list available languages to ensure your chosen language is installed (e.g., `fra` for French).

```bash
tesseract --version
tesseract --list-langs
```

**Install a utility to convert PDF pages into images**

For PDFs that require OCR, you need a utility to convert PDF pages into images. Install `poppler-utils`, which includes `pdftoppm`.

```bash
apt install poppler-utils
```

**Convert PDF to images**

Convert the PDF into JPEG images, with each page saved as a separate file. Each page will be named sequentially (e.g., `output-1.jpg`, `output-2.jpg`, etc.).

```bash
pdftoppm -jpeg your_file.pdf output
```

- **Tip**: Use a dedicated output directory to avoid overwriting existing files.
- **Alternative tools**: If `poppler-utils` isn’t available, consider using `ImageMagick`:

  ```bash
  convert -density 300 your_file.pdf output-%04d.jpg
  ```

**Perform OCR on a single image**

Run Tesseract OCR on an image to extract text. Specify the language using the `-l` option.

```bash
tesseract output-1.jpg output-text -l fra
```

The extracted text will be saved in `output-text.txt`.

**Perform OCR on multiple images**

For multi-page PDFs, process all images in a loop. This extracts text from each image and saves it to a separate `.txt` file.

```bash
for img in output-*.jpg; do
    tesseract "$img" "${img%.jpg}" -l fra
done
```

- **Note**: The `${img%.jpg}` syntax removes the `.jpg` extension, ensuring each `.txt` file matches its corresponding image.

**Combine all text files**

Merge the text from all processed pages into a single file. This is useful for assembling the full content of the PDF.

```bash
cat output-*.txt > complete_text.txt
```

If filenames are out of order, use a sorting approach before merging:

```bash
ls output-*.txt | sort -V | xargs cat > complete_text.txt
```

**Troubleshooting and Tips**

**If Tesseract doesn’t recognize text**:

- Ensure the images have sufficient quality and resolution. Use `-r` with `pdftoppm` to increase the DPI (e.g., `-r 300` for 300 DPI).
- Try additional Tesseract language packs for better recognition of specific text styles.

**Using `pdftotext` for simpler PDFs**:  
 If the PDF contains selectable text (not just images), `pdftotext` from `poppler-utils` can extract text directly without OCR.

```bash
pdftotext your_file.pdf output.txt
```

Replace `convert` with `magick` for newer versions.

**Verify language codes for Tesseract**:  
 You can find a list of supported languages on the [Tesseract GitHub page](https://github.com/tesseract-ocr/tesseract).
