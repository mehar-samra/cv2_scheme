;;; Test cases for OpenCV Scheme.
;;;

;;; Open Web cam
(define webcam (cv2.videocapture 0))

;;; Open Robotics video
(define video (cv2.videocapture "/Users/mehar/Downloads/GOPR1142.MP4"))

;;; Show n images by recursion
(define (show device n)
    (cond 
      ( (>= n 1) 
        (begin
          ;;; Capture an image from web camera
          (define img (device 'read))
          ;;; Display the image
          (cv2.imshow "Scheme CV2 Demo" img)
          ;;; Recursive call
          (show device (- n 1))
        ) 
      )
    )
)

;;; show video
(show video 10)

;;; show web camera
(show webcam 100)
