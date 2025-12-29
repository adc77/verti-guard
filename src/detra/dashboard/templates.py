"""Dashboard JSON templates for Datadog."""

from typing import Any


def get_dashboard_definition(app_name: str, env: str = "production") -> dict[str, Any]:
    """
    Generate the complete dashboard definition.

    Args:
        app_name: Application name for the dashboard.
        env: Environment (development, staging, production).

    Returns:
        Complete dashboard JSON definition.
    """
    return {
        "title": f"{app_name} - LLM Observability",
        "description": "End-to-end LLM observability dashboard with health metrics, security signals, and actionable insights",
        "widgets": [
            {
                "definition": {
                    "title": "Overall Adherence Score",
                    "type": "query_value",
                    "requests": [
                        {
                            "q": "avg:detra.node.adherence_score{$env,$node}",
                        }
                    ],
                    "precision": 2,
                },
                "layout": {"x": 0, "y": 0, "width": 47, "height": 15},
            },
            {
                "definition": {
                    "title": "Flag Rate",
                    "type": "query_value",
                    "requests": [
                        {
                            "q": "sum:detra.node.flagged{$env,$node}.as_count() / sum:detra.node.calls{$env,$node}.as_count() * 100",
                        }
                    ],
                    "precision": 1,
                    "custom_unit": "%",
                },
                "layout": {"x": 47, "y": 0, "width": 47, "height": 15},
            },
            {
                "definition": {
                    "title": "Error Rate",
                    "type": "query_value",
                    "requests": [
                        {
                            "q": "sum:detra.node.calls{status:error,$env,$node}.as_count() / sum:detra.node.calls{$env,$node}.as_count() * 100",
                        }
                    ],
                    "precision": 1,
                    "custom_unit": "%",
                },
                "layout": {"x": 94, "y": 0, "width": 47, "height": 15},
            },
            {
                "definition": {
                    "title": "Average Latency",
                    "type": "query_value",
                    "requests": [
                        {
                            "q": "avg:detra.node.latency{$env,$node}",
                        }
                    ],
                    "precision": 0,
                    "custom_unit": "ms",
                },
                "layout": {"x": 141, "y": 0, "width": 47, "height": 15},
            },
            {
                "definition": {
                    "title": "Adherence Score Over Time",
                    "type": "timeseries",
                    "requests": [
                        {
                            "q": "avg:detra.node.adherence_score{$env,$node} by {node}",
                            "display_type": "line",
                        }
                    ],
                    "yaxis": {
                        "min": "0",
                        "max": "1",
                    },
                    "markers": [
                        {
                            "value": "y = 0.85",
                            "display_type": "warning dashed",
                        },
                        {
                            "value": "y = 0.70",
                            "display_type": "error dashed",
                        },
                    ],
                },
                "layout": {"x": 0, "y": 15, "width": 188, "height": 30},
            },
            {
                "definition": {
                    "title": "Flags by Category",
                    "type": "toplist",
                    "requests": [
                        {
                            "q": "sum:detra.node.flagged{$env,$node} by {category}.as_count()",
                            "style": {
                                "palette": "warm",
                            },
                        }
                    ],
                },
                "layout": {"x": 0, "y": 45, "width": 94, "height": 30},
            },
            {
                "definition": {
                    "title": "Flags by Node",
                    "type": "toplist",
                    "requests": [
                        {
                            "q": "sum:detra.node.flagged{$env,$node} by {node}.as_count()",
                            "style": {
                                "palette": "orange",
                            },
                        }
                    ],
                },
                "layout": {"x": 94, "y": 45, "width": 94, "height": 30},
            },
            {
                "definition": {
                    "title": "Security Issues by Type",
                    "type": "toplist",
                    "requests": [
                        {
                            "q": "sum:detra.security.issues{$env,$node} by {check}.as_count()",
                            "style": {
                                "palette": "red",
                            },
                        }
                    ],
                },
                "layout": {"x": 0, "y": 75, "width": 94, "height": 30},
            },
            {
                "definition": {
                    "title": "Security Issues Over Time",
                    "type": "timeseries",
                    "requests": [
                        {
                            "q": "sum:detra.security.issues{$env,$node} by {severity}.as_count()",
                            "display_type": "bars",
                        }
                    ],
                },
                "layout": {"x": 94, "y": 75, "width": 94, "height": 30},
            },
            {
                "definition": {
                    "title": "Latency Distribution",
                    "type": "heatmap",
                    "requests": [
                        {
                            "q": "avg:detra.node.latency{$env,$node} by {node}",
                        }
                    ],
                },
                "layout": {"x": 0, "y": 105, "width": 94, "height": 30},
            },
            {
                "definition": {
                    "title": "Latency Percentiles",
                    "type": "timeseries",
                    "requests": [
                        {
                            "q": "p50:detra.node.latency{$env,$node}",
                            "display_type": "line",
                        },
                        {
                            "q": "p95:detra.node.latency{$env,$node}",
                            "display_type": "line",
                        },
                        {
                            "q": "p99:detra.node.latency{$env,$node}",
                            "display_type": "line",
                        },
                    ],
                },
                "layout": {"x": 94, "y": 105, "width": 94, "height": 30},
            },
            {
                "definition": {
                    "title": "Evaluation Token Usage",
                    "type": "timeseries",
                    "requests": [
                        {
                            "q": "sum:detra.evaluation.tokens{$env,$node}.as_count()",
                            "display_type": "bars",
                        }
                    ],
                },
                "layout": {"x": 0, "y": 135, "width": 188, "height": 30},
            },
            {
                "definition": {
                    "title": "Call Volume by Node",
                    "type": "timeseries",
                    "requests": [
                        {
                            "q": "sum:detra.node.calls{$env,$node} by {node}.as_count()",
                            "display_type": "bars",
                        }
                    ],
                },
                "layout": {"x": 0, "y": 165, "width": 188, "height": 30},
            },
            {
                "definition": {
                    "title": "Recent Events",
                    "type": "event_stream",
                    "query": "source:detra",
                    "event_size": "s",
                },
                "layout": {"x": 0, "y": 195, "width": 188, "height": 30},
            },
            {
                "definition": {
                    "title": "Monitor Status",
                    "type": "manage_status",
                    "query": "*",
                    "sort": "status,asc",
                    "display_format": "countsAndList",
                },
                "layout": {"x": 0, "y": 225, "width": 188, "height": 30},
            },
        ],
        "template_variables": [
            {
                "name": "node",
                "prefix": "node",
                "default": "*",
            },
            {
                "name": "env",
                "prefix": "env",
                "default": env,
            },
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
        "title": f"{app_name} - LLM Observability (Minimal)",
        "description": "Essential LLM observability metrics",
        "widgets": [
            {
                "definition": {
                    "title": "Adherence Score",
                    "type": "query_value",
                    "requests": [
                        {
                            "q": "avg:detra.node.adherence_score{*}",
                        }
                    ],
                    "precision": 2,
                },
                "layout": {"x": 0, "y": 0, "width": 47, "height": 15},
            },
            {
                "definition": {
                    "title": "Adherence Over Time",
                    "type": "timeseries",
                    "requests": [
                        {
                            "q": "avg:detra.node.adherence_score{*}",
                            "display_type": "line",
                        }
                    ],
                    "yaxis": {
                        "min": "0",
                        "max": "1",
                    },
                },
                "layout": {"x": 0, "y": 15, "width": 188, "height": 30},
            },
            {
                "definition": {
                    "title": "Call Volume",
                    "type": "timeseries",
                    "requests": [
                        {
                            "q": "sum:detra.node.calls{*}.as_count()",
                            "display_type": "bars",
                        }
                    ],
                },
                "layout": {"x": 0, "y": 45, "width": 188, "height": 30},
            },
        ],
        "layout_type": "free",
        "notify_list": [],
    }
