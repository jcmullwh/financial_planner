# git-tree.ps1
<#
.SYNOPSIS
    Generates a folder structure of the current Git repository excluding ignored files.

.DESCRIPTION
    This script uses 'git ls-files' to list all tracked files and constructs a tree-like
    folder structure, respecting the .gitignore rules.

.USAGE
    .\git-tree.ps1

.OUTPUTS
    Writes the folder structure to the console.

.NOTES
    Ensure you're running this script from the root directory of your Git repository.
#>

# Function to Print the Tree Recursively
function Print-Tree {
    param (
        [Parameter(Mandatory=$true)]
        [hashtable]$Node,

        [string]$Prefix = ""
    )

    $keys = $Node.Keys | Sort-Object
    $count = $keys.Count
    $i = 0

    foreach ($key in $keys) {
        $i++
        $isLast = $i -eq $count
        if ($isLast) {
            Write-Output "$Prefix|-- $key"
            $newPrefix = "$Prefix    "
        }
        else {
            Write-Output "$Prefix|-- $key"
            $newPrefix = "$Prefix|   "
        }

        if ($Node[$key].Count -gt 0) {
            Print-Tree -Node $Node[$key] -Prefix $newPrefix
        }
    }
}

# Verify Git Repository
try {
    $gitRoot = git rev-parse --show-toplevel 2>$null
    if (-not $gitRoot) {
        throw "Not inside a Git repository."
    }
}
catch {
    Write-Error "Error: $_"
    exit 1
}

# Navigate to Git Root
Set-Location $gitRoot

# Retrieve Tracked Files
try {
    $files = git ls-files
    if (-not $files) {
        throw "No tracked files found."
    }
}
catch {
    Write-Error "Error retrieving tracked files: $_"
    exit 1
}

# Initialize an Empty Hashtable for the Tree
$tree = @{}

# Build the Tree Structure
foreach ($file in $files) {
    $parts = $file -split '/'

    $current = $tree
    foreach ($part in $parts) {
        if (-not $current.ContainsKey($part)) {
            $current[$part] = @{}
        }
        $current = $current[$part]
    }
}

# Print the Tree
Print-Tree -Node $tree
