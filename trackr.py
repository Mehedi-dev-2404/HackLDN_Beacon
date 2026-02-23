# trackr_scraper_final.py
import requests
import json
from datetime import datetime
import time
import os
import pandas as pd

class TrackrScraper:
    def __init__(self):
        self.api_url = "https://api.the-trackr.com/programmes"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
            'Referer': 'https://app.the-trackr.com/uk-technology/summer-internships'
        }
        
    def fetch_category(self, category_type, season="2026"):
        """Fetch jobs for a specific category"""
        
        params = {
            "region": "UK",
            "industry": "Technology",
            "season": season,
            "type": category_type
        }
        
        print(f"📥 Fetching {category_type}...")
        
        try:
            response = requests.get(
                self.api_url, 
                params=params, 
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code == 200:
                jobs = response.json()
                
                # Clean and format the data
                formatted_jobs = []
                for job in jobs:
                    # Extract company name properly
                    company_name = "Unknown"
                    if isinstance(job.get('company'), dict):
                        company_name = job['company'].get('name', 'Unknown')
                    elif isinstance(job.get('company'), str):
                        company_name = job['company']
                    
                    # Create a clean job object with only what we need
                    clean_job = {
                        'id': job.get('id', ''),
                        'company': company_name,
                        'programme': job.get('name', ''),
                        'category': category_type,
                        'season': season,
                        'region': job.get('region', 'UK'),
                        'locations': ', '.join(job.get('locations', [])) if job.get('locations') else 'UK',
                        'opening_date': job.get('openingDate', 'TBA'),
                        'closing_date': job.get('closingDate', 'TBA'),
                        'url': job.get('url', ''),
                        'format': job.get('format', ''),
                        'eligibility': job.get('eligibility', ''),
                        'cv_required': 'Yes' if job.get('cv') else 'No',
                        'rolling': job.get('rolling', False),
                        'scraped_date': datetime.now().isoformat()
                    }
                    
                    # Only add if we have essential data
                    if clean_job['company'] != 'Unknown' and clean_job['programme']:
                        formatted_jobs.append(clean_job)
                
                print(f"✅ Found {len(formatted_jobs)} jobs in {category_type}")
                return formatted_jobs
            else:
                print(f"❌ Failed with status {response.status_code}")
                return []
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return []
    
    def fetch_all_categories(self, season="2026"):
        """Fetch all job categories"""
        
        categories = [
            "summer-internships",
            "industrial-placements",
            "graduate-programmes",
            "spring-weeks"
        ]
        
        all_jobs = []
        
        for category in categories:
            jobs = self.fetch_category(category, season)
            all_jobs.extend(jobs)
            
            # Be polite to the server - wait between requests
            time.sleep(2)
        
        return all_jobs
    
    def save_jobs(self, jobs):
        """Save jobs to files for your website"""
        
        if not jobs:
            print("❌ No jobs to save")
            return False
        
        # Create data directory
        os.makedirs('data', exist_ok=True)
        
        # Save timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # 1. Save all jobs (for archive)
        filename = f'data/trackr_jobs_{timestamp}.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(jobs, f, indent=2, ensure_ascii=False)
        print(f"💾 Saved full archive to {filename}")
        
        # 2. Save latest jobs (for your website to load)
        with open('data/jobs_latest.json', 'w', encoding='utf-8') as f:
            json.dump(jobs, f, indent=2, ensure_ascii=False)
        print(f"💾 Saved latest to data/jobs_latest.json")
        
        # 3. Save as CSV for easy viewing
        df = pd.DataFrame(jobs)
        df.to_csv('data/jobs_latest.csv', index=False)
        print(f"💾 Saved to data/jobs_latest.csv")
        
        # 4. Create category-specific files for your homepage
        categories = {}
        for job in jobs:
            cat = job['category']
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(job)
        
        for cat, cat_jobs in categories.items():
            safe_name = cat.replace('-', '_')
            with open(f'data/jobs_{safe_name}.json', 'w', encoding='utf-8') as f:
                # Keep only first 50 for performance
                json.dump(cat_jobs[:50], f, indent=2)
            print(f"💾 Saved {len(cat_jobs[:50])} jobs to data/jobs_{safe_name}.json")
        
        # 5. Create a summary file for your homepage (3 most recent)
        recent_jobs = sorted(jobs, 
                           key=lambda x: x.get('scraped_date', ''), 
                           reverse=True)[:3]
        with open('data/recent_jobs.json', 'w', encoding='utf-8') as f:
            json.dump(recent_jobs, f, indent=2)
        print(f"💾 Saved 3 recent jobs to data/recent_jobs.json")
        
        return True

def main():
    print("=" * 60)
    print("🚀 TRACKR JOB SCRAPER")
    print("=" * 60)
    
    scraper = TrackrScraper()
    
    # Ask which season to scrape
    season = input("\n📅 Enter season year (default 2026): ").strip()
    if not season:
        season = "2026"
    
    # Ask which categories
    print("\n📋 Categories:")
    print("1. All categories")
    print("2. Summer Internships only")
    print("3. Industrial Placements only")
    print("4. Graduate Programmes only")
    print("5. Spring Weeks only")
    
    choice = input("\nSelect option (1-5): ").strip()
    
    if choice == "1":
        jobs = scraper.fetch_all_categories(season)
    elif choice == "2":
        jobs = scraper.fetch_category("summer-internships", season)
    elif choice == "3":
        jobs = scraper.fetch_category("industrial-placements", season)
    elif choice == "4":
        jobs = scraper.fetch_category("graduate-programmes", season)
    elif choice == "5":
        jobs = scraper.fetch_category("spring-weeks", season)
    else:
        print("❌ Invalid choice")
        return
    
    if jobs:
        scraper.save_jobs(jobs)
        print(f"\n✅ COMPLETE! Total jobs: {len(jobs)}")
        
        # Show sample
        print("\n📋 Sample jobs:")
        for i, job in enumerate(jobs[:3]):
            print(f"\n  {i+1}. {job['company']} - {job['programme']}")
            print(f"     📅 Closes: {job['closing_date']}")
    else:
        print("❌ No jobs found")

if __name__ == "__main__":
    main()