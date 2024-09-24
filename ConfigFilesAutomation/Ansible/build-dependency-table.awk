BEGIN {
    # Print the header for the columns
    print "Rocky8\t\tUbuntu22.04\t\tWindows10"
}

{
    # Group packages under their respective container
    if ($1 == "rocky8_container") rocky8 = rocky8 $2 "\t"
    else if ($1 == "ubuntu22_04_container") ubuntu = ubuntu $2 "\t"
    else if ($1 == "windows10_container") windows = windows $2 "\t"
}

END {
    # Split each container list of packages into arrays
    n = split(rocky8, rocky8_arr, "\t")
    m = split(ubuntu, ubuntu_arr, "\t")
    p = split(windows, windows_arr, "\t")

    # Determine the maximum number of packages in any container
    max = (n > m ? (n > p ? n : p) : (m > p ? m : p))

    # Loop through the arrays and print the columns
    for (i = 1; i <= max; i++) {
        print (i <= n ? rocky8_arr[i] : "") "\t\t" (i <= m ? ubuntu_arr[i] : "") "\t\t" (i <= p ? windows_arr[i] : "")
    }
}
