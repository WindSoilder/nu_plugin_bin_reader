def find-plugin-path [] {
    open $nu.plugin-path | find nu_plugin_bin_reader | split column ' ' | get column2 | ansi strip | get 0
}

# get all libs available on kaitai gallery, the output is sorted in alphabetical order
export def all-libs [] {
    [
        "android_bootldr_asus", "android_bootldr_huawei", "android_bootldr_qcom", "android_img",
        "android_nanoapp_header", "android_opengl_shaders_cache", "android_sparse", "android_super",
        "dex", "android_dto", "chrome_pak", "cpio_old_le", "gzip", "lzh", "mozilla_mar",
        "phar_without_stub", "rar", "rpm", "xar", "zip", "zisofs", "bcd", "bytes_with_io",
        "dos_datetime", "riff", "utf8_string", "vlq_base128_be", "vlq_base128_le", "dbf", "gettext_mo",
        "sqlite3", "tsm", "dos_mz", "mbr_partition_table", "vfat", "elf", "java_class", "mach_o",
        "microsoft_pe", "python_pyc_27", "swf", "uefi_te", "apm_partition_table", "apple_single_double",
        "btrfs_stream", "cramfs", "ext2", "gpt_partition_table", "iso9660", "luks", "lvm2", "tr_dos_image",
        "vdi", "vmware_vmdk", "zx_spectrum_tap", "andes_firmware", "broadcom_trx", "ines", "uimage",
        "grub2_font", "pcf_font", "ttf", "allegro_dat", "doom_wad", "dune_2_pak", "fallout2_dat",
        "fallout_dat", "ftl_dat", "gran_turismo_vol", "heaps_pak", "heroes_of_might_and_magic_agg",
        "heroes_of_might_and_magic_bmp", "minecraft_nbt", "quake_mdl", "quake_pak", "renderware_binary_stream",
        "saints_row_2_vpp_pc", "warcraft_2_pud", "shapefile_index", "shapefile_main", "dtb", "edid",
        "mifare_classic", "bmp", "dicom", "exif", "gif", "gimp_brush", "icc_4", "ico", "jpeg", "nitf",
        "pcx", "pcx_dcx", "png", "psx_tim", "tga", "wmf", "xwd", "glibc_utmp", "sudoers_ts", "systemd_journal",
        "aix_utmp", "hashcat_restore", "mcap", "windows_evt_log", "compressed_resource", "dcmp_0", "dcmp_1",
        "dcmp_2", "dcmp_variable_length_integer", "ds_store", "mac_os_resource_snd", "resource_fork", "au", "avi",
        "blender_blend", "creative_voice_file", "fasttracker_xm_module", "genmidi_op2", "id3v1_1", "id3v2_3",
        "id3v2_4", "magicavoxel_vox", "ogg", "quicktime_mov", "s3m", "standard_midi_file", "stl", "vp8_ivf",
        "wav", "bitcoin_transaction", "dime_message", "dns_packet", "ethernet_frame", "hccap", "hccapx", "icmp_packet",
        "ipv4_packet", "ipv6_packet", "microsoft_network_monitor_v2", "packet_ppi", "pcap", "protocol_body",
        "rtcp_payload", "rtp_packet", "rtpdump", "some_ip", "some_ip_container", "some_ip_sd", "some_ip_sd_entries",
        "some_ip_sd_options", "tcp_segment", "tls_client_hello", "udp_datagram", "websocket", "avantes_roh60", "nt_mdt",
        "nt_mdt_pal", "specpr", "efivar_signature_list", "openpgp_message", "ssh_public_key", "asn1_der", "bson",
        "google_protobuf", "microsoft_cfb", "msgpack", "php_serialized_value", "python_pickle", "ruby_marshal", "regf",
        "windows_lnk_file", "windows_minidump", "windows_resource_file", "windows_shell_items", "windows_systemtime"
    ] | sort
}

def get-lib-path [name: string] {
    let plugin_dir = (find-plugin-path | path dirname)
    $plugin_dir | path join "reader" $"($name).py"
}

# download binary parsing lib from kaitai gallery
export def fetch-lib [
    name: string  # lib name
] {
    if (not (all-libs | any {|$it| $it == $name})) {
        error make -u {msg: $"Library `($name)` is not supported, run `all-libs` to check for all available libs"}
    }
    echo $"going to download lib ($name)"
    let url = $"https://formats.kaitai.io/($name)/src/python/($name).py"
    let content = http get $url
    let target_path = get-lib-path $name
    echo $"download complete, begin to save"
    $content | save -f $target_path
    echo "done"
}

# remove binary parsing lib local
export def remove-lib [
    name: string  # lib name
] {
    let lib_path = get-lib-path $name
    if ($lib_path | path exists) {
        rm $lib_path
    } else {
        error make -u  {msg: $"Library ($name) is not exists"}
    }
}

# remove all binary parsing libs
export def remove-all-libs [] {
    let plugin_dir = (find-plugin-path | path dirname)
    rm -rf ($plugin_dir | path join "reader" "*")
}

# fetch all libs available on kaitai gallery
#
# Note: It's recommend to use `fetch-lib` to download the lib you need
export def fetch-all-libs [] {
    all-libs | each { |it| fetch-bin-lib $it }
}
