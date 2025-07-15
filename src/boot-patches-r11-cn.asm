.psp
.relativeinclude off

.open "BOOT.BIN.patched", 0x08803F60

;; Do not call sceImposeSetLanguageMode to avoid overriding language settings
.org 0x0880B580
.area 4*1
    nop; 0x0880B580: relocation-cleared
.endarea; 0x0880B584
.orga 0x14AFD8 :: .fill 8*1; clear 0x0880B580


;; Decrease line spacing in fullscreen text.
;.org 0x0881CCB0
;.area 4
;	addiu	a2,v0,-0x1
;.endarea


;; Fix the text bug for "All Choices:". (Inlined strcpy didn't copy the last char)
.org 0x08828084
.area 4*1
	lw	v0,0x14(v1)
.endarea :: .skip 4*1 :: .area 4*1
	sw	v0,0x14(s0)
.endarea; 0x08828090


;; Increases the size of the glyph buffer for choice lines from 22 to 44
;; (Caused some choice lines to be overwritten by the following ones)
.org 0x0881FE54
.area 4*2
	sll	v0,a2,0x6
	sll	a2,a2,0x2
.endarea; 0x0881FE5C


.close
