#!/usr/bin/env python3
"""
🏥 Health Check and Monitoring Script for Global News Digest AI

This script provides comprehensive health monitoring for the application.
"""

import asyncio
import aiohttp
import psycopg2
import time
import json
import logging
from datetime import datetime
from typing import Dict, List, Any
import os
from dataclasses import dataclass

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('health_check.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class HealthStatus:
    service: str
    status: str
    response_time: float
    details: Dict[str, Any]
    timestamp: datetime

class HealthChecker:
    def __init__(self):
        self.backend_url = os.getenv('BACKEND_URL', 'http://localhost:8000')
        self.frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:3000')
        self.db_host = os.getenv('DB_HOST', 'localhost')
        self.db_port = int(os.getenv('DB_PORT', 5432))
        self.db_name = os.getenv('DB_NAME', 'news_digest')
        self.db_user = os.getenv('DB_USER', 'postgres')
        self.db_password = os.getenv('DB_PASSWORD', '')
        
    async def check_backend_health(self) -> HealthStatus:
        """Check backend API health"""
        start_time = time.time()
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.backend_url}/health", timeout=10) as response:
                    response_time = time.time() - start_time
                    
                    if response.status == 200:
                        data = await response.json()
                        return HealthStatus(
                            service="backend",
                            status="healthy",
                            response_time=response_time,
                            details=data,
                            timestamp=datetime.now()
                        )
                    else:
                        return HealthStatus(
                            service="backend",
                            status="unhealthy",
                            response_time=response_time,
                            details={"error": f"HTTP {response.status}"},
                            timestamp=datetime.now()
                        )
                        
        except Exception as e:
            response_time = time.time() - start_time
            return HealthStatus(
                service="backend",
                status="unhealthy",
                response_time=response_time,
                details={"error": str(e)},
                timestamp=datetime.now()
            )
    
    async def check_frontend_health(self) -> HealthStatus:
        """Check frontend availability"""
        start_time = time.time()
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.frontend_url, timeout=10) as response:
                    response_time = time.time() - start_time
                    
                    if response.status == 200:
                        return HealthStatus(
                            service="frontend",
                            status="healthy",
                            response_time=response_time,
                            details={"status_code": response.status},
                            timestamp=datetime.now()
                        )
                    else:
                        return HealthStatus(
                            service="frontend",
                            status="unhealthy",
                            response_time=response_time,
                            details={"error": f"HTTP {response.status}"},
                            timestamp=datetime.now()
                        )
                        
        except Exception as e:
            response_time = time.time() - start_time
            return HealthStatus(
                service="frontend",
                status="unhealthy",
                response_time=response_time,
                details={"error": str(e)},
                timestamp=datetime.now()
            )
    
    def check_database_health(self) -> HealthStatus:
        """Check database connectivity"""
        start_time = time.time()
        
        try:
            conn = psycopg2.connect(
                host=self.db_host,
                port=self.db_port,
                database=self.db_name,
                user=self.db_user,
                password=self.db_password,
                connect_timeout=10
            )
            
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
            
            # Get additional database info
            cursor.execute("SELECT COUNT(*) FROM articles")
            article_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM user_interactions")
            interaction_count = cursor.fetchone()[0]
            
            cursor.close()
            conn.close()
            
            response_time = time.time() - start_time
            
            return HealthStatus(
                service="database",
                status="healthy",
                response_time=response_time,
                details={
                    "article_count": article_count,
                    "interaction_count": interaction_count
                },
                timestamp=datetime.now()
            )
            
        except Exception as e:
            response_time = time.time() - start_time
            return HealthStatus(
                service="database",
                status="unhealthy",
                response_time=response_time,
                details={"error": str(e)},
                timestamp=datetime.now()
            )
    
    async def check_api_endpoints(self) -> List[HealthStatus]:
        """Check specific API endpoints"""
        endpoints = [
            "/api/news/articles",
            "/api/news/trending",
            "/api/news/stats"
        ]
        
        results = []
        
        for endpoint in endpoints:
            start_time = time.time()
            
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"{self.backend_url}{endpoint}", timeout=10) as response:
                        response_time = time.time() - start_time
                        
                        if response.status == 200:
                            data = await response.json()
                            results.append(HealthStatus(
                                service=f"api{endpoint}",
                                status="healthy",
                                response_time=response_time,
                                details={"data_length": len(data) if isinstance(data, list) else 1},
                                timestamp=datetime.now()
                            ))
                        else:
                            results.append(HealthStatus(
                                service=f"api{endpoint}",
                                status="unhealthy",
                                response_time=response_time,
                                details={"error": f"HTTP {response.status}"},
                                timestamp=datetime.now()
                            ))
                            
            except Exception as e:
                response_time = time.time() - start_time
                results.append(HealthStatus(
                    service=f"api{endpoint}",
                    status="unhealthy",
                    response_time=response_time,
                    details={"error": str(e)},
                    timestamp=datetime.now()
                ))
        
        return results
    
    async def run_comprehensive_check(self) -> Dict[str, Any]:
        """Run comprehensive health check"""
        logger.info("Starting comprehensive health check...")
        
        # Run all checks
        backend_health = await self.check_backend_health()
        frontend_health = await self.check_frontend_health()
        database_health = self.check_database_health()
        api_health = await self.check_api_endpoints()
        
        # Compile results
        all_checks = [backend_health, frontend_health, database_health] + api_health
        
        healthy_count = sum(1 for check in all_checks if check.status == "healthy")
        total_count = len(all_checks)
        
        overall_status = "healthy" if healthy_count == total_count else "degraded" if healthy_count > 0 else "unhealthy"
        
        results = {
            "overall_status": overall_status,
            "healthy_services": healthy_count,
            "total_services": total_count,
            "timestamp": datetime.now().isoformat(),
            "checks": {
                "backend": {
                    "status": backend_health.status,
                    "response_time": backend_health.response_time,
                    "details": backend_health.details
                },
                "frontend": {
                    "status": frontend_health.status,
                    "response_time": frontend_health.response_time,
                    "details": frontend_health.details
                },
                "database": {
                    "status": database_health.status,
                    "response_time": database_health.response_time,
                    "details": database_health.details
                },
                "api_endpoints": [
                    {
                        "service": check.service,
                        "status": check.status,
                        "response_time": check.response_time,
                        "details": check.details
                    } for check in api_health
                ]
            }
        }
        
        # Log results
        logger.info(f"Health check completed: {overall_status} ({healthy_count}/{total_count} services healthy)")
        
        # Save results to file
        with open('health_report.json', 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        return results
    
    def print_health_report(self, results: Dict[str, Any]):
        """Print formatted health report"""
        print("\n" + "="*60)
        print("🏥 GLOBAL NEWS DIGEST AI - HEALTH REPORT")
        print("="*60)
        
        # Overall status
        status_emoji = "✅" if results["overall_status"] == "healthy" else "⚠️" if results["overall_status"] == "degraded" else "❌"
        print(f"\n{status_emoji} Overall Status: {results['overall_status'].upper()}")
        print(f"📊 Services: {results['healthy_services']}/{results['total_services']} healthy")
        print(f"🕐 Timestamp: {results['timestamp']}")
        
        print("\n📋 Service Details:")
        print("-" * 40)
        
        # Backend
        backend = results["checks"]["backend"]
        status_icon = "✅" if backend["status"] == "healthy" else "❌"
        print(f"{status_icon} Backend API: {backend['status']} ({backend['response_time']:.3f}s)")
        
        # Frontend
        frontend = results["checks"]["frontend"]
        status_icon = "✅" if frontend["status"] == "healthy" else "❌"
        print(f"{status_icon} Frontend: {frontend['status']} ({frontend['response_time']:.3f}s)")
        
        # Database
        database = results["checks"]["database"]
        status_icon = "✅" if database["status"] == "healthy" else "❌"
        print(f"{status_icon} Database: {database['status']} ({database['response_time']:.3f}s)")
        if database["status"] == "healthy":
            print(f"   📰 Articles: {database['details'].get('article_count', 'N/A')}")
            print(f"   👥 Interactions: {database['details'].get('interaction_count', 'N/A')}")
        
        # API Endpoints
        print(f"\n🔗 API Endpoints:")
        for endpoint in results["checks"]["api_endpoints"]:
            status_icon = "✅" if endpoint["status"] == "healthy" else "❌"
            service_name = endpoint["service"].replace("api/api/news/", "").replace("api", "")
            print(f"{status_icon} {service_name}: {endpoint['status']} ({endpoint['response_time']:.3f}s)")
        
        print("\n" + "="*60)

async def main():
    """Main function"""
    checker = HealthChecker()
    
    try:
        results = await checker.run_comprehensive_check()
        checker.print_health_report(results)
        
        # Exit with appropriate code
        if results["overall_status"] == "healthy":
            exit(0)
        elif results["overall_status"] == "degraded":
            exit(1)
        else:
            exit(2)
            
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        print(f"❌ Health check failed: {e}")
        exit(3)

if __name__ == "__main__":
    asyncio.run(main())
