# Datasheets

One PDF per part, named `<PART>.pdf` (e.g. `TPS63001.pdf`). Stored with Git LFS (see `.gitattributes`).
Record the revision and date printed on the PDF in `parts/constraints/<PART>.yaml`. When a vendor
publishes a new revision, add it as `<PART>_rev<X>.pdf` and re-review the constraints file.

Non-part references kept here: `hardware-design-with-rp2350.pdf`, `pico-2-datasheet.pdf`, `pico-2-w-schematic.pdf`,
`USB-Type-C-Spec-R2.0.pdf` (USB Type-C Cable and Connector Specification Release 2.0, August 2019, from usb.org;
used for CC Rd Table 4-25 p.236 and USB 2.0 pin use Table 3-5 p.69).

Capacitor characteristic sheets (Samsung Electro-Mechanics, 1 page, DC-bias curve): `CL10A475KO8NNNC.pdf`
(dated 2013-09-10, from https://www.ceramic-capacitor.com/pdf-d7/cl10a475ko8nnnc.pdf) and `CL10A106MA8NRNC.pdf`
(undated, from https://www.compel.ru/infosheet/SAMSUNG/CL10A106MA8NRNC), both fetched 2026-10-15 for D-007 / S3-7.

USB 2.0 (P5-14, fetched 2026-10-15 from usb.org, `https://www.usb.org/sites/default/files/usb_20_20250603.zip`):
`USB-2.0-Spec.pdf` (Universal Serial Bus Specification Revision 2.0, `usb_20.pdf` in the zip; used for §7.2.4.1
p.177, §7.2.4.2 p.177-178, Table 7-7 C_RPB p.179 and Note 9 p.184) and `USB-2.0-ECN-Device-Capacitance.pdf`
(ECN "Device Capacitance", same zip; C_RPB 1.0-10.0 µF across 0-5.25 V, p.2).
`CL31A106KBHNNNE.pdf`: Samsung characteristic sheet (dated 2013-09-10, DC-bias curve), from
https://www.ceramic-capacitor.com/pdf-f7/cl31a106kbhnnne.pdf, fetched 2026-10-15 (D-009, C20).
`TDK105CBJ475MV-F.pdf`: Taiyo Yuden spec sheet + electrical characteristics (2 pages, DC-bias curve; page 2 marked
AQC19J26-08D), from https://datasheet.lcsc.com/datasheet/pdf/c61da25d4a37446bb4cac279b9ea2540.pdf?productCode=C22385335,
fetched 2026-10-17 (D-025, C18/C27).
`DFE201612P-2R2M.pdf`: Murata spec "DFE201612P Type" JE243A-0033-01 (Reference Only, 9 pages: dimensions p.1, ratings p.2,
recommended PCB pattern p.5, notes ~p.7), from the LCSC/JLC public datasheet link for C79317
(https://jlcpcb.com/api/file/downloadByFileSystemAccessId/8588955072436834304), fetched 2026-10-23 (D-030, L2).
`CL21A106KAYNNNE.pdf`: Samsung characteristic sheet (1 page, DC-bias graph 3), from
https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/503/CL21A106KAYNNNE_Char.pdf, fetched 2026-10-23 (D-030, C20).
