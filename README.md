# AutoSCAD - OpenSCAD AUTO_MAKE_STL alternative

Alternative way of executing AUTO_MAKE_STL for OpenSCAD with the following advantages :

- Easy-to-call standalone script
    ```shell
    make_stl.py file.scad
    ```

- Allows specifying the parameters to call the module with, avoiding the hassle of creating one function per configuration
    ```scad
    module my_module(w, l, h, matw, math, xn, yn, hcap) // AUTO_MAKE_STL[790][190][105][20][2][1][1][10]
    ```

- The generated stl file name will contain both the name of the module called and the parameters

- Allows specifying ranges and lists for parameters. Combinatorial configurations are accepted
    ```scad
    module my_module(w, l, h, matw, math, xn, yn, hcap) // AUTO_MAKE_STL[790][190][105][20][2][1:4][1:2][10]

    // This example will generate 8 files
    ```

- Still compatible with multiple calls per files

- Easy customization of misc. aspects per-project since it's a short python script

- Parallelized execution of OpenSCAD

## License

GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
