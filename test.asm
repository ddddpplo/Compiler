ExitProcess PROTO
.data
.code
main PROC
	sub rsp, 40
	mov rcx, 42
	call ExitProcess
main ENDP
END
