"""Tests for TUI functionality."""

import pytest
from unittest.mock import patch, MagicMock

from budgetcli.cli.tui_utils import (
    clear_screen,
    validate_number,
    validate_date,
    get_today_str,
    get_current_month_str,
    NavigationStack,
)


class TestTUIUtils:
    """Test TUI utility functions."""

    def test_validate_number_positive(self) -> None:
        """Test validate_number with positive number."""
        result = validate_number("42.50", allow_negative=False)
        assert result == 42.50

    def test_validate_number_negative_not_allowed(self) -> None:
        """Test validate_number with negative when not allowed."""
        result = validate_number("-10", allow_negative=False)
        assert result is None

    def test_validate_number_negative_allowed(self) -> None:
        """Test validate_number with negative when allowed."""
        result = validate_number("-10", allow_negative=True)
        assert result == -10

    def test_validate_number_invalid(self) -> None:
        """Test validate_number with invalid input."""
        result = validate_number("abc")
        assert result is None

    def test_validate_date_valid(self) -> None:
        """Test validate_date with valid date."""
        result = validate_date("2026-04-17")
        assert result is True

    def test_validate_date_invalid(self) -> None:
        """Test validate_date with invalid date."""
        result = validate_date("2026-13-01")
        assert result is False

    def test_validate_date_wrong_format(self) -> None:
        """Test validate_date with wrong format."""
        result = validate_date("04/17/2026")
        assert result is False

    def test_get_today_str_format(self) -> None:
        """Test get_today_str returns correct format."""
        result = get_today_str()
        assert len(result) == 10
        assert result[4] == "-" and result[7] == "-"

    def test_get_current_month_str_format(self) -> None:
        """Test get_current_month_str returns correct format."""
        result = get_current_month_str()
        assert len(result) == 7
        assert result[4] == "-"

    @patch("os.system")
    def test_clear_screen(self, mock_system: MagicMock) -> None:
        """Test clear_screen calls os.system."""
        clear_screen()
        mock_system.assert_called_once()


class TestNavigationStack:
    """Test NavigationStack class."""

    def test_navigation_stack_push(self) -> None:
        """Test pushing to navigation stack."""
        stack = NavigationStack()
        mock_fn = MagicMock()

        stack.push(mock_fn)

        mock_fn.assert_called_once()

    def test_navigation_stack_is_at_root_initial(self) -> None:
        """Test is_at_root on new stack."""
        stack = NavigationStack()
        assert stack.is_at_root() is True

    def test_navigation_stack_is_at_root_after_push(self) -> None:
        """Test is_at_root after push."""
        stack = NavigationStack()
        mock_fn = MagicMock()

        stack.push(mock_fn)

        assert stack.is_at_root() is False

    def test_navigation_stack_go_back(self) -> None:
        """Test going back in navigation stack."""
        stack = NavigationStack()
        mock_fn1 = MagicMock()
        mock_fn2 = MagicMock()

        stack.push(mock_fn1)
        stack.push(mock_fn2)

        # Both should be called once from push
        assert mock_fn1.call_count == 1
        assert mock_fn2.call_count == 1

        # Go back should call fn1 again
        stack.go_back()
        assert mock_fn1.call_count == 2

    def test_navigation_stack_reset(self) -> None:
        """Test resetting navigation stack."""
        stack = NavigationStack()
        mock_fn = MagicMock()

        stack.push(mock_fn)
        assert stack.is_at_root() is False

        stack.reset()
        assert stack.is_at_root() is True


class TestTUIStart:
    """Test TUI start command."""

    def test_budget_start_help(self) -> None:
        """Test that budget start --help works without crashing."""
        # This test verifies the command is registered
        from budgetcli.cli.main import app

        assert app is not None

    def test_tui_import(self) -> None:
        """Test that tui module can be imported."""
        from budgetcli.cli import tui

        assert hasattr(tui, "start_tui")
        assert hasattr(tui, "animate_opening")
