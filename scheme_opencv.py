import cv2
import numpy
from scheme_eval_apply import *
from scheme_utils import *
from scheme_classes import *
from scheme_builtins import *

def add_opencv_special_forms(SPECIAL_FORMS):
    SPECIAL_FORMS["cv2.videocapture"] = do_cv2_videocapture_form
    SPECIAL_FORMS["cv2.imshow"] = do_cv2_imshow_form


class MatProcedure(LambdaProcedure):
    """An OpenCV class defined by a lambda expression"""

    def __init__(self, mat, env):
        """A OpenCV Mat procedure"""
        assert isinstance(env, Frame), "env must be of type Frame"
        self.env = env
        self.mat = mat

    def __str__(self):
        return str(Pair('cv2.mat', Pair(self.mat, nil)))

    def __repr__(self):
        return 'MatProcedure({0}, {2})'.format(
            repr(self.mat), repr(self.env))

    def scheme_apply(self, method, env):
        validate_type(arg, lambda x: scheme_stringp(x), 0, 'MatProcedure')
        
        if(method == "size"):
            return self.mat.size

        raise SchemeError('unknown method call: {0}.{1}'.format(type(self), method))


class VideoCaptureProcedure(LambdaProcedure):
    """An OpenCV class defined by a lambda expression."""

    def __init__(self, arg, env):
        """A OpenCV videocapture procedure with arg"""
        assert isinstance(env, Frame), "env must be of type Frame"

        from scheme_utils import validate_type, scheme_listp
        validate_type(arg, lambda x: scheme_numberp(x) or scheme_stringp(x), 0, 'VideoCaptureProcedure')

        # Not sure why strings have quotes around them, strip them
        if scheme_stringp(arg):
            arg = arg.strip('\"')
            arg = arg.strip("\'")

        self.arg = arg
        self.env = env

        self.cap = cv2.VideoCapture(self.arg)

    def __str__(self):
        return str(Pair('cv2.videocapture', Pair(self.arg, nil)))

    def __repr__(self):
        return 'VideoCaptureProcedure({0}, {2})'.format(
            repr(self.arg), repr(self.env))

    def scheme_apply(self, method, env):
        validate_form(method, 1)
        if(method.first == "read"):
            ret, frame = self.cap.read()
            return MatProcedure(frame, env)
        raise SchemeError('unknown method call: {0}.{1}'.format(type(self), method.first))



def do_cv2_videocapture_form(expressions, env):
    """Evaluate an OpenCV VideoCapture form."""
    validate_form(expressions, 1)
    return VideoCaptureProcedure(expressions.first, env)


def do_cv2_imshow_form(expressions, env):
    """Evaluate an OpenCV image show form."""
    validate_form(expressions, 2)
    window_name = expressions.first
    if not isinstance(window_name, str):
        raise SchemeError('first argument should be string not', type(window_name), window_name)
    mat_name = expressions.rest.first
    if not isinstance(mat_name, str):
        raise SchemeError('second argument should be matrix', type(mat_name), mat_name)
    mat_procedure = scheme_eval(mat_name, env)
    if not isinstance(mat_procedure, MatProcedure):
        raise SchemeError('second argument should be matrix', type(mat_procedure), mat_procedure)
    
    # sometimes the image was invalid, so ignore it
    if type(mat_procedure.mat) == type(None):
        return

    # side effect to show the image
    cv2.imshow(window_name, mat_procedure.mat)

    # Need to wait key otherwise will now show up
    cv2.waitKey(1)


