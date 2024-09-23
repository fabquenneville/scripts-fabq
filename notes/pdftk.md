# pdftk

## Table of Contents

- [pdftk](#pdftk)
  - [Table of Contents](#table-of-contents)
  - [Basic Commands](#basic-commands)

## Basic Commands

**Merge PDFs**

To merge two PDFs, use:

```
pdftk file1.pdf file2.pdf cat output merged.pdf
```

**Append PDF**

To append one PDF to another, use:

```
pdftk A=first.pdf B=second.pdf cat A B output combined.pdf
```

**Cut pages from PDF**

To only keep the first page:

```
pdftk file1.pdf cat 1-1 output output.pdf
```

**Split PDF**

To split a PDF into single pages, use:

```
pdftk input.pdf burst output page_%02d.pdf
```

**Rotate PDF Pages**

To rotate pages in a PDF, use:

```
pdftk input.pdf cat 1-endsouth output rotated.pdf
```

**Encrypt PDF**

To encrypt a PDF with a password, use:

```
pdftk input.pdf output encrypted.pdf user_pw yourpassword
```
