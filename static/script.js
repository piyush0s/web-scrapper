class GoogleMapsLeadScraper {
  constructor() {
    this.leads = [];
    this.initializeEventListeners();
  }

  initializeEventListeners() {
    document.getElementById("scrapeForm").addEventListener("submit", (e) => {
      e.preventDefault();
      this.startScraping();
    });

    document.getElementById("exportBtn").addEventListener("click", () => {
      this.exportToCSV();
    });
  }

  async startScraping() {
    const query = document.getElementById("query").value;
    const location = document.getElementById("location").value;
    const maxResults = document.getElementById("maxResults").value;

    if (!query) {
      this.showError("Please enter a search query");
      return;
    }

    this.showLoading(true);
    this.clearResults();

    try {
      const response = await fetch("/scrape", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          query,
          location,
          maxResults,
        }),
      });

      const data = await response.json();

      if (data.error) {
        this.showError(data.error);
        return;
      }

      this.leads = data.leads;
      this.displayResults();
      this.updateStats(data.stats);
      this.showExportSection(true);
    } catch (error) {
      this.showError("An error occurred while scraping. Please try again.");
      console.error("Scraping error:", error);
    } finally {
      this.showLoading(false);
    }
  }

  displayResults() {
    const resultsContent = document.getElementById("resultsContent");
    resultsContent.innerHTML = "";

    this.leads.forEach((lead, index) => {
      const leadElement = this.createLeadElement(lead, index);
      resultsContent.appendChild(leadElement);
    });
  }

  createLeadElement(lead, index) {
    const div = document.createElement("div");
    div.className = "lead-item fade-in";
    div.style.animationDelay = `${index * 0.1}s`;

    const stars = "⭐".repeat(Math.floor(lead.rating || 0));

    div.innerHTML = `
      <div class="lead-name">${lead.name}</div>
      <div class="lead-info">
        <i>📍</i> ${lead.address || 'N/A'}
      </div>
      ${lead.phone ? `<div class="lead-info"><i>📞</i> ${lead.phone}</div>` : ''}
      ${lead.website ? `<div class="lead-info"><i>🌐</i> <a href="${lead.website}" target="_blank">${lead.website}</a></div>` : ''}
      ${lead.rating ? `
        <div class="rating">
          <span class="stars">${stars}</span>
          <span>${lead.rating} ${lead.reviews_count ? `(${lead.reviews_count} reviews)` : ''}</span>
        </div>
      ` : ''}
    `;

    return div;
  }

  updateStats(stats) {
    document.getElementById("totalLeads").textContent = stats.total;
    document.getElementById("withPhone").textContent = stats.with_phone;
    document.getElementById("withWebsite").textContent = stats.with_website;
    document.getElementById("stats").style.display = "grid";
  }

  exportToCSV() {
    if (this.leads.length === 0) {
      alert("No leads to export");
      return;
    }

    const headers = ["Name", "Address", "Phone", "Website", "Rating", "Reviews", "Category"];
    const csvContent = [
      headers.join(","),
      ...this.leads.map(lead =>
        [
          `"${lead.name}"`,
          `"${lead.address || ''}"`,
          `"${lead.phone || ''}"`,
          `"${lead.website || ''}"`,
          lead.rating || '',
          lead.reviews_count || '',
          `"${lead.category || ''}"`
        ].join(",")
      )
    ].join("\n");

    const blob = new Blob([csvContent], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `leads_${new Date().toISOString().split("T")[0]}.csv`;
    a.click();
    URL.revokeObjectURL(url);
    this.showSuccessMessage("CSV file downloaded successfully!");
  }

  showLoading(show) {
    const loading = document.getElementById("loading");
    const scrapeBtn = document.getElementById("scrapeBtn");
    loading.style.display = show ? "flex" : "none";
    scrapeBtn.disabled = show;
    scrapeBtn.textContent = show ? "Scraping..." : " Start Scraping";
  }

  showExportSection(show) {
    document.getElementById("exportSection").style.display = show ? "block" : "none";
  }

  clearResults() {
    document.getElementById("resultsContent").innerHTML = `
      <div style="padding: 40px; text-align: center; color: #a0aec0;">
        <div style="font-size: 3rem; margin-bottom: 15px;">🎯</div>
        <p>Your scraped leads will appear here</p>
      </div>
    `;
    document.getElementById("stats").style.display = "none";
  }

  showError(message) {
    document.getElementById("resultsContent").innerHTML = `
      <div style="padding: 40px; text-align: center; color: #e53e3e;">
        <div style="font-size: 3rem; margin-bottom: 15px;">❌</div>
        <p>${message}</p>
      </div>
    `;
  }

  showSuccessMessage(message) {
    const successDiv = document.createElement("div");
    successDiv.className = "alert alert-info";
    successDiv.innerHTML = `<strong> Success:</strong> ${message}`;
    document.getElementById("exportSection").appendChild(successDiv);
    setTimeout(() => successDiv.remove(), 3000);
  }
}

// Initialize when DOM is loaded
document.addEventListener("DOMContentLoaded", () => {
  new GoogleMapsLeadScraper();
});