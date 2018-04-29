# -*- coding: utf-8 -*-
########################################################################
# <LUXPY: a Python package for lighting and color science.>
# Copyright (C) <2017>  <Kevin A.G. Smet> (ksmet1977 at gmail.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#########################################################################
"""
###############################################################################
# _COLORTF_DEFAULT_WHITE_POINT: ndarray with XYZ values of default white point 
                                (equi-energy white) for color transformation 
                                if none is supplied.

# colortf(): Calculates conversion between any two color spaces 
             for which functions xyz_to_...() and ..._to_xyz() are defined.
###############################################################################

Created on Fri Jun 30 18:34:34 2017

@author: Kevin A.G. Smet (ksmet1977 at gmail.com)
"""

from luxpy import *
__all__ = ['_COLORTF_DEFAULT_WHITE_POINT','colortf']


_COLORTF_DEFAULT_WHITE_POINT = np.array([100.0, 100.0, 100.0]) # ill. E white point

#------------------------------------------------------------------------------------------------
def colortf(data, tf = _CSPACE, fwtf = {}, bwtf = {}, **kwargs):
    """
    Wrapper function to perform various color transformations.
    
    Args:
        :data: ndarray
        :tf: _CSPACE or str specifying transform type, optional
            E.g. tf = 'spd>xyz' or 'spd>Yuv' or 'Yuv>cct' 
                or 'Yuv' or 'Yxy' or ...
            If tf is for example 'Yuv', it is assumed to be a transformation 
                of type: 'xyz>Yuv'
        :fwtf: dict with parameters (keys) and values required 
                by some color transformations for the forward transform: 
                i.e. 'xyz>...'
        :bwtf: dict with parameters (keys) and values required 
                by some color transformations for the backward transform: 
                i.e. '...>xyz'

    Returns:
        :returns: ndarray with data transformed to new color space
        
    Note:
        For the forward transform ('xyz>...'), one can input the keyword 
        arguments specifying the transform parameters directly without having 
        to use the dict :fwtf: (should be empty!) 
        [i.e. kwargs overwrites empty fwtf dict]
    """
    #data = np2d(data)
    tf = tf.split('>')
    if len(tf) == 1:
        if not bool(fwtf):
            fwtf = kwargs
        return globals()['{}_to_{}'.format('xyz', tf[0])](data,**fwtf)
    else:
        if not bool(fwtf):
            fwtf = kwargs
        bwfcn = globals()['{}_to_{}'.format(tf[0], 'xyz')]
        fwfcn = globals()['{}_to_{}'.format('xyz', tf[1])]
        return fwfcn(bwfcn(data,**bwtf),**fwtf)   


#def colortf(data, tf = _CSPACE, tfa0 = {}, tfa1 = {}, **kwargs):
#    """
#    Wrapper function to perform various color transformations.
#    
#    Args:
#        :data: ndarray
#        :tf: str specifying transform type, optional
#            E.g. tf = 'spd>xyz' or 'spd>Yuv' or 'Yuv>cct' or 'Yuv' or 'Yxy' or ...
#            If tf is for example 'Yuv' it is assumed to be a transformation of type: 'xyz>Yuv'
#        :tfa0: dict with parameters (keys) and values required by some color transformations ('...>xyz')
#        :tfa1: dict with parameters (keys) and values required by some color transformations ('xyz>...')
#
#    Returns:
#        :returns: ndarray with data transformed to new color space
#    """
#    data = np2d(data)
#    tf = tf.split('>')
#    if len(tf)>1:
#        for ii in range(len(tf)):    
#            if (ii%2 == 1):
#                out_ = tf[ii]
#                in_ = 'xyz'
#                tfa = tfa0
#            else:
#                out_ = 'xyz'
#                in_ = tf[ii]
#                tfa = tfa1
#            data = globals()['{}_to_{}'.format(in_, out_)](data,**tfa)
#
#	
#    else:
#        data = globals()['{}_to_{}'.format('xyz', tf[0])](data,**tfa0)
#    return data   