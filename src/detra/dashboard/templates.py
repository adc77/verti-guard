"""Dashboard JSON templates for Datadog."""

from typing import Any


def get_dashboard_definition(app_name: str, env: str = "production") -> dict[str, Any]:
    """
    Generate the standard dashboard definition.

    Args:
        app_name: Application name for the dashboard.
        env: Environment (development, staging, production).

    Returns:
        Complete dashboard JSON definition.
    """
    return {
        "title": f"Detra: {app_name} - LLM Observability",
        "description": "LLM observability with adherence scoring, error tracking, and security monitoring",
        "widgets": [
            # Row 1: Key Metrics
            {
                "definition": {
                    "title": "Adherence Score",
                    "type": "query_value",
                    "requests": [{"q": "avg:detra.node.adherence_score{*}"}],
                    "precision": 2,
                    "conditional_formats": [
                        {"comparator": ">=", "value": 0.85, "palette": "white_on_green"},
                        {"comparator": ">=", "value": 0.70, "palette": "white_on_yellow"},
                        {"comparator": "<", "value": 0.70, "palette": "white_on_red"},
                    ],
                },
                "layout": {"x": 0, "y": 0, "width": 3, "height": 2},
            },
            {
                "definition": {
                    "title": "Flag Rate",
                    "type": "query_value",
                    "requests": [
                        {"q": "sum:detra.node.flagged{*}.as_count() / sum:detra.node.calls{*}.as_count() * 100"}
                    ],
                    "precision": 1,
                    "custom_unit": "%",
                },
                "layout": {"x": 3, "y": 0, "width": 3, "height": 2},
            },
            {
                "definition": {
                    "title": "Error Count",
                    "type": "query_value",
                    "requests": [{"q": "sum:detra.errors.count{*}.as_count()"}],
                    "precision": 0,
                    "conditional_formats": [
                        {"comparator": "<=", "value": 5, "palette": "white_on_green"},
                        {"comparator": ">", "value": 5, "palette": "white_on_red"},
                    ],
                },
                "layout": {"x": 6, "y": 0, "width": 3, "height": 2},
            },
            {
                "definition": {
                    "title": "Avg Latency",
                    "type": "query_value",
                    "requests": [{"q": "avg:detra.node.latency{*}"}],
                    "precision": 0,
                    "custom_unit": "ms",
                },
                "layout": {"x": 9, "y": 0, "width": 3, "height": 2},
            },

            # Row 2: Adherence Trends
            {
                "definition": {
                    "title": "Adherence Score Over Time",
                    "type": "timeseries",
                    "requests": [
                        {"q": "avg:detra.node.adherence_score{*} by {node}", "display_type": "line"}
                    ],
                    "markers": [
                        {"value": "y = 0.85", "display_type": "warning dashed"},
                        {"value": "y = 0.70", "display_type": "error dashed"},
                    ],
                    "yaxis": {"min": "0", "max": "1"},
                },
                "layout": {"x": 0, "y": 2, "width": 12, "height": 3},
            },

            # Row 3: Flags Analysis
            {
                "definition": {
                    "title": "Flags by Category",
                    "type": "toplist",
                    "requests": [
                        {"q": "sum:detra.node.flagged{*} by {category}.as_count()", "style": {"palette": "warm"}}
                    ],
                },
                "layout": {"x": 0, "y": 5, "width": 6, "height": 3},
            },
            {
                "definition": {
                    "title": "Flags by Node",
                    "type": "toplist",
                    "requests": [
                        {"q": "sum:detra.node.flagged{*} by {node}.as_count()", "style": {"palette": "orange"}}
                    ],
                },
                "layout": {"x": 6, "y": 5, "width": 6, "height": 3},
            },

            # Row 4: Errors
            {
                "definition": {
                    "title": "Errors Over Time",
                    "type": "timeseries",
                    "requests": [
                        {"q": "sum:detra.errors.count{*}.as_count()", "display_type": "bars"}
                    ],
                },
                "layout": {"x": 0, "y": 8, "width": 6, "height": 3},
            },
            {
                "definition": {
                    "title": "Top Error Types",
                    "type": "toplist",
                    "requests": [
                        {"q": "sum:detra.errors.count{*} by {exception_type}.as_count()", "style": {"palette": "warm"}}
                    ],
                },
                "layout": {"x": 6, "y": 8, "width": 6, "height": 3},
            },

            # Row 5: Security
            {
                "definition": {
                    "title": "Security Issues by Type",
                    "type": "toplist",
                    "requests": [
                        {"q": "sum:detra.security.issues{*} by {check}.as_count()", "style": {"palette": "red"}}
                    ],
                },
                "layout": {"x": 0, "y": 11, "width": 6, "height": 3},
            },
            {
                "definition": {
                    "title": "Security Over Time",
                    "type": "timeseries",
                    "requests": [
                        {"q": "sum:detra.security.issues{*} by {severity}.as_count()", "display_type": "bars"}
                    ],
                },
                "layout": {"x": 6, "y": 11, "width": 6, "height": 3},
            },

            # Row 6: Performance
            {
                "definition": {
                    "title": "Latency Distribution",
                    "type": "heatmap",
                    "requests": [{"q": "avg:detra.node.latency{*} by {node}"}],
                },
                "layout": {"x": 0, "y": 14, "width": 6, "height": 3},
            },
            {
                "definition": {
                    "title": "Latency Percentiles",
                    "type": "timeseries",
                    "requests": [
                        {"q": "p50:detra.node.latency{*}", "display_type": "line"},
                        {"q": "p95:detra.node.latency{*}", "display_type": "line"},
                        {"q": "p99:detra.node.latency{*}", "display_type": "line"},
                    ],
                },
                "layout": {"x": 6, "y": 14, "width": 6, "height": 3},
            },

            # Row 7: Agent Workflows
            {
                "definition": {
                    "title": "Agent Workflow Duration",
                    "type": "timeseries",
                    "requests": [
                        {"q": "avg:detra.agent.workflow.duration_ms{*} by {agent}", "display_type": "line"}
                    ],
                },
                "layout": {"x": 0, "y": 17, "width": 6, "height": 3},
            },
            {
                "definition": {
                    "title": "Tool Calls per Workflow",
                    "type": "timeseries",
                    "requests": [
                        {"q": "avg:detra.agent.tool_calls{*} by {agent}", "display_type": "bars"}
                    ],
                },
                "layout": {"x": 6, "y": 17, "width": 6, "height": 3},
            },

            # Row 8: Call Volume
            {
                "definition": {
                    "title": "Call Volume by Node",
                    "type": "timeseries",
                    "requests": [
                        {"q": "sum:detra.node.calls{*} by {node}.as_count()", "display_type": "bars"}
                    ],
                },
                "layout": {"x": 0, "y": 20, "width": 12, "height": 3},
            },

            # Row 9: Events
            {
                "definition": {
                    "title": "Recent Events",
                    "type": "event_stream",
                    "query": "sources:detra",
                    "event_size": "s",
                },
                "layout": {"x": 0, "y": 23, "width": 12, "height": 3},
            },

            # Row 10: Monitor Status
            {
                "definition": {
                    "title": "Monitor Status",
                    "type": "manage_status",
                    "query": "tag:(source:detra)",
                    "sort": "status,asc",
                    "display_format": "countsAndList",
                },
                "layout": {"x": 0, "y": 26, "width": 12, "height": 3},
            },
        ],
        "template_variables": [
            {"name": "node", "prefix": "node", "default": "*"},
            {"name": "env", "prefix": "env", "default": env},
        ],
        "layout_type": "free",
        "notify_list": [],
    }


def get_minimal_dashboard_definition(app_name: str) -> dict[str, Any]:
    """
    Generate a minimal dashboard with essential widgets.

    Args:
        app_name: Application name.

    Returns:
        Minimal dashboard JSON definition.
    """
    return {
        "title": f"Detra: {app_name} (Minimal)",
        "description": "Essential LLM observability metrics",
        "widgets": [
            {
                "definition": {
                    "title": "Adherence Score",
                    "type": "query_value",
                    "requests": [{"q": "avg:detra.node.adherence_score{*}"}],
                    "precision": 2,
                    "conditional_formats": [
                        {"comparator": ">=", "value": 0.85, "palette": "white_on_green"},
                        {"comparator": "<", "value": 0.85, "palette": "white_on_red"},
                    ],
                },
                "layout": {"x": 0, "y": 0, "width": 4, "height": 2},
            },
            {
                "definition": {
                    "title": "Error Count",
                    "type": "query_value",
                    "requests": [{"q": "sum:detra.errors.count{*}.as_count()"}],
                    "precision": 0,
                },
                "layout": {"x": 4, "y": 0, "width": 4, "height": 2},
            },
            {
                "definition": {
                    "title": "Avg Latency",
                    "type": "query_value",
                    "requests": [{"q": "avg:detra.node.latency{*}"}],
                    "precision": 0,
                    "custom_unit": "ms",
                },
                "layout": {"x": 8, "y": 0, "width": 4, "height": 2},
            },
            {
                "definition": {
                    "title": "Adherence Over Time",
                    "type": "timeseries",
                    "requests": [{"q": "avg:detra.node.adherence_score{*}", "display_type": "line"}],
                },
                "layout": {"x": 0, "y": 2, "width": 12, "height": 3},
            },
            {
                "definition": {
                    "title": "Call Volume",
                    "type": "timeseries",
                    "requests": [{"q": "sum:detra.node.calls{*}.as_count()", "display_type": "bars"}],
                },
                "layout": {"x": 0, "y": 5, "width": 12, "height": 3},
            },
        ],
        "layout_type": "free",
        "notify_list": [],
    }
