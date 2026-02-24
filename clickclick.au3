#Region ;**** Directives created by AutoIt3Wrapper_GUI ****
#AutoIt3Wrapper_Compression=0
#AutoIt3Wrapper_UseX64=y
#EndRegion ;**** Directives created by AutoIt3Wrapper_GUI ****

; Set the Escape hotkey to terminate the script.
;HotKeySet("{ESC}", "_Terminate")

HotKeySet("{F3}", "Example")

while 1
    sleep(100)
wend


Func Example()
    Local $aMgp = 0

    $aMgp = MouseGetPos()

    MouseClick('left', $aMgp[0], $aMgp[1], 1, 0)
    MouseMove($aMgp[0], $aMgp[1] + 23, 0)
    Sleep(50)
EndFunc   ;==>Example

;Func _Terminate()
;    Exit
;EndFunc   ;==>_Terminate
