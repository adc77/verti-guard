#!/usr/bin/env python3
"""
Traffic Generator for VertiGuard Demo

Generates realistic traffic patterns to demonstrate detection rules:
1. Normal requests (passes all checks)
2. Semantic violations (hallucinations, made-up entities)
3. PII exposure attempts
4. High latency scenarios
5. Format violations

Run: python scripts/traffic_generator.py
"""

import asyncio
import json
import os
import random
import sys
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import google.genai as genai
import structlog

import vertiguard
from dotenv import load_dotenv

load_dotenv()

logger = structlog.get_logger()


class TrafficGenerator:
    """
    Generates diverse traffic patterns to test VertiGuard detection rules.

    Traffic patterns:
    - 60% Normal (should pass)
    - 15% Semantic violations (hallucinations, wrong data)
    - 10% PII exposure attempts
    - 10% Format violations
    - 5% High latency (simulated slow responses)
    """

    def __init__(self, config_path: str):
        """Initialize traffic generator."""
        self.vg = vertiguard.init(config_path)

        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not set")
        self.client = genai.Client(api_key=api_key)

        self.stats = {
            "total": 0,
            "normal": 0,
            "semantic_violation": 0,
            "pii_exposure": 0,
            "format_violation": 0,
            "high_latency": 0,
            "flagged": 0,
            "errors": 0,
        }

    async def generate_traffic(
        self,
        num_requests: int = 50,
        delay_between_requests: float = 2.0,
    ) -> dict:
        """
        Generate traffic with mixed patterns.

        Args:
            num_requests: Total number of requests to generate.
            delay_between_requests: Delay between requests in seconds.

        Returns:
            Statistics dictionary.
        """
        logger.info(
            "Starting traffic generation",
            num_requests=num_requests,
            delay=delay_between_requests,
        )

        for i in range(num_requests):
            request_type = self._select_request_type()
            logger.info(f"Request {i+1}/{num_requests}", type=request_type)

            try:
                await self._execute_request(request_type)
                self.stats["total"] += 1
                self.stats[request_type] += 1
            except Exception as e:
                logger.error("Request failed", error=str(e), type=request_type)
                self.stats["errors"] += 1

            # Delay between requests
            if i < num_requests - 1:
                await asyncio.sleep(delay_between_requests)

        # Print final stats
        self._print_stats()

        return self.stats

    def _select_request_type(self) -> str:
        """Select request type based on probability distribution."""
        rand = random.random()

        if rand < 0.60:
            return "normal"
        elif rand < 0.75:
            return "semantic_violation"
        elif rand < 0.85:
            return "pii_exposure"
        elif rand < 0.95:
            return "format_violation"
        else:
            return "high_latency"

    async def _execute_request(self, request_type: str):
        """Execute a request based on type."""
        if request_type == "normal":
            await self._normal_request()
        elif request_type == "semantic_violation":
            await self._semantic_violation()
        elif request_type == "pii_exposure":
            await self._pii_exposure()
        elif request_type == "format_violation":
            await self._format_violation()
        elif request_type == "high_latency":
            await self._high_latency_request()

    async def _normal_request(self):
        """Generate a normal request that should pass all checks."""
        document = self._get_sample_contract()

        # Use the decorated functions from example app
        result = await self.extract_entities_traced(document)

        logger.info("Normal request completed", has_parties=bool(result.get("parties")))

    async def _semantic_violation(self):
        """Generate request with hallucinations/made-up data."""
        # Inject a document with intentionally wrong information
        bad_document = """
CONSULTING AGREEMENT

This Agreement is between TechCorp Solutions Inc. and LegalTech Partners LLC.

TERM: January 1, 2024 to December 31, 2025

COMPENSATION: $50,000 per month payable on the 1st of each month.

The CEO of TechCorp is Sarah Williams and the CFO is John Anderson.

Contact: ceo@techcorp.com, (555) 123-4567
"""
        # This will likely trigger hallucinations as the LLM might add details not in doc
        result = await self.extract_entities_malicious(bad_document)

        logger.info("Semantic violation request completed")

    async def _pii_exposure(self):
        """Generate request that attempts to extract PII."""
        pii_document = """
Employment Agreement

Employee: Jane Smith
SSN: 123-45-6789
Email: jane.smith@email.com
Phone: (555) 987-6543
Credit Card: 4532-1234-5678-9012

Annual Salary: $150,000
"""
        result = await self.extract_entities_traced(pii_document)

        logger.info("PII exposure request completed")

    async def _format_violation(self):
        """Generate request that produces invalid format."""
        # Ask for a response that will violate format expectations
        document = "Contract between A and B for services."

        # Directly call with minimal info to trigger format errors
        result = await self.extract_entities_minimal(document)

        logger.info("Format violation request completed")

    async def _high_latency_request(self):
        """Simulate high latency request."""
        document = """
COMPLEX MERGER AGREEMENT

This is an extremely complex 50-page merger agreement between
multiple parties with extensive terms, conditions, schedules,
and appendices that would take a long time to process...
""" * 20  # Make it really long

        # Add artificial delay
        await asyncio.sleep(3.0)

        result = await self.extract_entities_traced(document)

        logger.info("High latency request completed")

    # Traced functions (decorated with VertiGuard)

    @vertiguard.trace("extract_entities")
    async def extract_entities_traced(self, document: str) -> dict:
        """Extract entities (normal flow)."""
        prompt = f"""Extract entities from this document as JSON:
{{
  "parties": ["Party 1", "Party 2"],
  "dates": ["2024-01-15"],
  "amounts": ["$10,000"]
}}

Document:
{document}

Return ONLY valid JSON:"""

        response = await self._call_llm(prompt)
        return self._parse_json(response)

    @vertiguard.trace("extract_entities")
    async def extract_entities_malicious(self, document: str) -> dict:
        """Extract entities (with potential hallucinations)."""
        # Deliberately vague prompt that encourages hallucinations
        prompt = f"""Look at this document and tell me about the parties, dates, and money involved.
Be creative and thorough.

{document}

Give me JSON:"""

        response = await self._call_llm(prompt)
        return self._parse_json(response)

    @vertiguard.trace("extract_entities")
    async def extract_entities_minimal(self, document: str) -> dict:
        """Extract entities with minimal prompt (format violations likely)."""
        prompt = f"Entities in: {document}"

        response = await self._call_llm(prompt)
        # Return malformed response
        return {"raw": response, "malformed": True}

    async def _call_llm(self, prompt: str) -> str:
        """Call Gemini API."""
        loop = asyncio.get_event_loop()

        def generate():
            response = self.client.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt,
            )
            if hasattr(response, "text"):
                return response.text
            elif hasattr(response, "candidates") and response.candidates:
                candidate = response.candidates[0]
                if hasattr(candidate.content, "parts"):
                    parts = candidate.content.parts
                    if parts and hasattr(parts[0], "text"):
                        return parts[0].text
            return str(response)

        return await loop.run_in_executor(None, generate)

    def _parse_json(self, text: str) -> dict:
        """Parse JSON from LLM response."""
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()

        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return {"error": "Invalid JSON", "raw": text}

    def _get_sample_contract(self) -> str:
        """Get a sample contract for normal requests."""
        contracts = [
            """
CONSULTING AGREEMENT

Agreement between TechCorp Solutions Inc. and Advisory Partners LLC.
Effective Date: January 15, 2024
Term: 12 months
Monthly Fee: $10,000
""",
            """
SERVICE AGREEMENT

Provider: DataTech Services
Client: Enterprise Corp
Start Date: February 1, 2024
Annual Cost: $120,000
""",
            """
LICENSING AGREEMENT

Licensor: SoftwareCo Inc.
Licensee: Business Solutions Ltd.
License Fee: $5,000 per year
Term: 3 years starting March 1, 2024
"""
        ]
        return random.choice(contracts)

    def _print_stats(self):
        """Print traffic generation statistics."""
        print("\n" + "="*60)
        print("TRAFFIC GENERATION COMPLETE")
        print("="*60)
        print(f"Total Requests: {self.stats['total']}")
        print(f"Errors: {self.stats['errors']}")
        print("\nRequest Type Distribution:")
        print(f"  Normal:              {self.stats['normal']:3d} ({self.stats['normal']/max(self.stats['total'],1)*100:5.1f}%)")
        print(f"  Semantic Violations: {self.stats['semantic_violation']:3d} ({self.stats['semantic_violation']/max(self.stats['total'],1)*100:5.1f}%)")
        print(f"  PII Exposure:        {self.stats['pii_exposure']:3d} ({self.stats['pii_exposure']/max(self.stats['total'],1)*100:5.1f}%)")
        print(f"  Format Violations:   {self.stats['format_violation']:3d} ({self.stats['format_violation']/max(self.stats['total'],1)*100:5.1f}%)")
        print(f"  High Latency:        {self.stats['high_latency']:3d} ({self.stats['high_latency']/max(self.stats['total'],1)*100:5.1f}%)")
        print("="*60)
        print("\nCheck your Datadog dashboard for:")
        print("  - Adherence score trends")
        print("  - Flagged requests")
        print("  - Security issues detected")
        print("  - Latency distributions")
        print("  - Triggered monitors")
        print("="*60 + "\n")


async def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Generate traffic for VertiGuard demo")
    parser.add_argument(
        "--config",
        default="examples/legal_analyzer/vertiguard.yaml",
        help="Path to vertiguard.yaml config",
    )
    parser.add_argument(
        "--requests",
        type=int,
        default=50,
        help="Number of requests to generate",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=2.0,
        help="Delay between requests in seconds",
    )

    args = parser.parse_args()

    # Check environment variables
    required_vars = ["DD_API_KEY", "DD_APP_KEY", "GOOGLE_API_KEY"]
    missing = [v for v in required_vars if not os.getenv(v)]

    if missing:
        print(f"ERROR: Missing required environment variables: {', '.join(missing)}")
        print("\nSet them with:")
        for var in missing:
            print(f"  export {var}=your_key_here")
        sys.exit(1)

    print("="*60)
    print("VertiGuard Traffic Generator")
    print("="*60)
    print(f"Config: {args.config}")
    print(f"Requests: {args.requests}")
    print(f"Delay: {args.delay}s between requests")
    print("="*60 + "\n")

    generator = TrafficGenerator(args.config)

    try:
        stats = await generator.generate_traffic(
            num_requests=args.requests,
            delay_between_requests=args.delay,
        )

        # Close VertiGuard client
        await generator.vg.close()

        print("\n✅ Traffic generation completed successfully!")

    except KeyboardInterrupt:
        print("\n\n⚠️  Traffic generation interrupted by user")
        await generator.vg.close()
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
