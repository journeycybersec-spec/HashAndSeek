<h1>🔍 HashAndSeek</h1>
<h3>Advanced Forensic Hash Scanner &amp; File Discovery Tool</h3>

<p>
  <img src="https://img.shields.io/badge/status-active-brightgreen" alt="Status: active" />
  <img src="https://img.shields.io/badge/python-3.8%2B-blue" alt="Python 3.8+" />
  <img src="https://img.shields.io/badge/license-MIT-lightgrey" alt="License: MIT" />
  <img src="https://img.shields.io/badge/platform-linux%20%7C%20windows-lightgrey" alt="Platform: Linux | Windows" />
</p>

<hr />

<h2>🚀 Overview</h2>
<p><strong>HashAndSeek</strong> is a digital forensics utility designed to:</p>
<ul>
  <li>Calculate SHA256 or MD5 file hashes</li>
  <li>Search entire directory trees for files matching a known hash</li>
  <li>Log matching results</li>
  <li>Log skipped files due to permissions or device-file restrictions</li>
  <li>Display progress indicators, timers, and status messages</li>
  <li>Provide a clean, colorful, user-friendly UX with ASCII-art branding</li>
</ul>

<p>This tool is ideal for:</p>
<ul>
  <li>DFIR analysts</li>
  <li>OSINT &amp; cybersecurity investigators</li>
  <li>Malware analysts</li>
  <li>IT staff searching for duplicate or tampered files</li>
  <li>Anyone validating data integrity across large systems</li>
</ul>

<hr />

<h2>✨ Features</h2>

<h3>🔒 Hashing</h3>
<ul>
  <li>Calculate <strong>SHA256</strong> or <strong>MD5</strong> for any file</li>
  <li>Safe error handling</li>
  <li>Logging to <code>hash_search_log.txt</code></li>
</ul>

<h3>🔎 System-Wide Search</h3>
<ul>
  <li>Search any directory (or entire filesystem) for matching hashes</li>
  <li>Optionally skip restricted directories (<code>/proc</code>, <code>/sys</code>, <code>/dev</code>, etc.)</li>
  <li>Detects device files to avoid crashes</li>
  <li>Live progress spinner + elapsed time display</li>
  <li>Logs skipped files with reasons (<code>skipped_files_log.txt</code>)</li>
</ul>

<h3>🎨 User Interface</h3>
<ul>
  <li>Stylish ASCII-art header</li>
  <li>ANSI color-coded output</li>
  <li>Simple menu-driven UX</li>
  <li>Continuous loop until user exits</li>
</ul>

<h3>🗂 Logging</h3>
<table>
  <thead>
    <tr>
      <th>Log File</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>hash_search_log.txt</code></td>
      <td>Matches found during searches; hash results</td>
    </tr>
    <tr>
      <td><code>skipped_files_log.txt</code></td>
      <td>Device files or restricted files skipped during enumeration</td>
    </tr>
  </tbody>
</table>

<hr />

<h2>📦 Installation</h2>

<h3>Requirements</h3>
<ul>
  <li>Python <strong>3.8+</strong></li>
  <li>Linux or Windows</li>
  <li>No external libraries required</li>
</ul>

<h3>Clone the Repository</h3>
<pre><code class="language-bash">git clone https://github.com/yourusername/HashAndSeek.git
cd HashAndSeek
</code></pre>

<h3>Run the tool</h3>
<pre><code class="language-bash">python3 HashAndSeek.py
</code></pre>

<hr />

<h2>🖥 Usage Guide</h2>

<h3>Main Menu</h3>
<pre><code>1. Calculate file hash (SHA256 or MD5)
2. Search for matching hash in the system
3. Exit
</code></pre>

<h3>📁 1. Calculate File Hash</h3>
<p>You will be asked for:</p>
<ul>
  <li>File path</li>
  <li>Preferred hash algorithm</li>
</ul>

<p>Example:</p>
<pre><code>Enter the file path to hash: /home/user/file.bin
Choose hash algorithm (SHA256/MD5) [default: SHA256]:
</code></pre>

<p>Output:</p>
<pre><code>File hash (sha256): 2f776c4ac8e8f8702f...
</code></pre>

<h3>🔍 2. Search for Matching Hash</h3>
<p>You will be asked for:</p>
<ul>
  <li>Target hash</li>
  <li>Directory to search</li>
  <li>Whether to skip restricted directories</li>
</ul>

<p>Example:</p>
<pre><code>Enter the hash: d41d8cd98f00b204e9800998ecf8427e
Enter the directory to search (default is current directory):
Skip restricted access directories (like /sys, /proc)? (y/n): y
</code></pre>

<p>Live output:</p>
<pre><code>| Elapsed Time: 00:02:31 | Processed: 1200/4500
</code></pre>

<p>Match results:</p>
<pre><code>==== MATCHING FILES FOUND ====
 /home/user/Documents/sample.bin
</code></pre>

<hr />

<h2>📄 Logging Output Samples</h2>

<h3>Matches log</h3>
<pre><code>2025-12-03 14:22:11 - Match found: /var/log/auth.log | Hash (md5): d41d8cd98f00b204...
</code></pre>

<h3>Skipped files log</h3>
<pre><code>2025-12-03 14:22:13 - Skipping device file: /dev/zero
</code></pre>

<hr />

<h2>📜 License</h2>
<pre><code>Licensed under the Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0).
</code></pre>

<hr />

