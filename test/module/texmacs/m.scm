(display "module begin ...") (newline)
(texmacs-module (m))
; (define-module (m))
(provide-public (my-identity x) x)
(display "module end ...") (newline)
