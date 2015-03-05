#
# Project:   retdec-python
# Copyright: (c) 2015 by Petr Zemek <s3rvac@gmail.com> and contributors
# License:   MIT, see the LICENSE file for more details
#

"""Tests for the :mod:`retdec.fileinfo` module."""

import unittest
from unittest import mock

from retdec.conn import APIConnection
from retdec.exceptions import ResourceFailedError
from retdec.file import File
from retdec.fileinfo import Analysis
from retdec.fileinfo import Fileinfo
from tests.file_tests import AnyFile
from tests.service_tests import BaseServiceTests


class FileinfoRunAnalysisTests(BaseServiceTests):
    """Tests for :func:`retdec.fileinfo.Fileinfo.run_analysis()`."""

    def setUp(self):
        super().setUp()

        self.input_file_mock = mock.MagicMock(spec_set=File)

        self.fileinfo = Fileinfo(api_key='KEY')

    def test_creates_api_connection_with_correct_url_and_api_key(self):
        self.fileinfo.run_analysis(input_file=self.input_file_mock)

        self.APIConnectionMock.assert_called_once_with(
            'https://retdec.com/service/api/fileinfo/analyses',
            self.fileinfo.api_key
        )

    def test_verbose_is_set_to_0_when_not_given(self):
        self.fileinfo.run_analysis(input_file=self.input_file_mock)

        self.conn_mock.send_post_request.assert_called_once_with(
            '',
            params={'verbose': 0},
            files={'input': AnyFile()}
        )

    def test_verbose_is_set_to_0_when_given_but_false(self):
        self.fileinfo.run_analysis(
            input_file=self.input_file_mock,
            verbose=False
        )

        self.conn_mock.send_post_request.assert_called_once_with(
            '',
            params={'verbose': 0},
            files={'input': AnyFile()}
        )

    def test_verbose_is_set_to_1_when_given_and_true(self):
        self.fileinfo.run_analysis(
            input_file=self.input_file_mock,
            verbose=True
        )

        self.conn_mock.send_post_request.assert_called_once_with(
            '',
            params={'verbose': 1},
            files={'input': AnyFile()}
        )

    def test_uses_returned_id_to_initialize_analysis(self):
        self.conn_mock.send_post_request.return_value = {'id': 'ID'}

        analysis = self.fileinfo.run_analysis(
            input_file=self.input_file_mock
        )

        self.assertTrue(analysis.id, 'ID')

    def test_repr_returns_correct_value(self):
        self.assertEqual(
            repr(self.fileinfo),
            "<Fileinfo api_url='https://retdec.com/service/api'>"
        )


class AnalysisTests(unittest.TestCase):
    """Tests for :class:`retdec.fileinfo.Analysis`."""


class AnalysisWaitUntilFinishedTests(unittest.TestCase):
    """Tests for :func:`retdec.resource.Analysis.wait_until_finished()`."""

    def test_sends_correct_request_and_returns_when_resource_is_finished(self):
        conn_mock = mock.Mock(spec_set=APIConnection)
        conn_mock.send_get_request.return_value = {
            'finished': True,
            'succeeded': True,
            'failed': False,
            'error': None
        }
        a = Analysis('ID', conn_mock)

        a.wait_until_finished()

        conn_mock.send_get_request.assert_called_once_with('/ID/status')

    def test_raises_exception_by_default_when_resource_failed(self):
        conn_mock = mock.Mock(spec_set=APIConnection)
        conn_mock.send_get_request.return_value = {
            'finished': True,
            'succeeded': False,
            'failed': True,
            'error': 'error message'
        }
        a = Analysis('ID', conn_mock)

        with self.assertRaises(ResourceFailedError):
            a.wait_until_finished()

    def test_calls_on_failure_when_it_is_callable(self):
        conn_mock = mock.Mock(spec_set=APIConnection)
        conn_mock.send_get_request.return_value = {
            'finished': True,
            'succeeded': False,
            'failed': True,
            'error': 'error message'
        }
        a = Analysis('ID', conn_mock)
        on_failure_mock = mock.Mock()

        a.wait_until_finished(on_failure=on_failure_mock)

        on_failure_mock.assert_called_once_with('error message')

    def test_does_not_raise_exception_when_on_failure_is_none(self):
        conn_mock = mock.Mock(spec_set=APIConnection)
        conn_mock.send_get_request.return_value = {
            'finished': True,
            'succeeded': False,
            'failed': True,
            'error': 'error message'
        }
        a = Analysis('ID', conn_mock)

        a.wait_until_finished(on_failure=None)
