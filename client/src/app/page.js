"use client";
import { useState, useEffect } from "react";

export default function Home() {
  const [file, setFile] = useState(null);
  const [asciiArt, setAsciiArt] = useState("");
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState([]);

  useEffect(() => { fetchHistory(); }, []);

  const fetchHistory = async () => {
    try {
      const res = await fetch("http://127.0.0.1:5000/api/grimoire");
      const data = await res.json();
      setHistory(data);
    } catch (err) { console.error("System offline..."); }
  };

  const handleTransmute = async () => {
    if (!file) return;
    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://127.0.0.1:5000/api/transmute", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      setAsciiArt(data.art);
      fetchHistory();
    } catch (error) { alert("TRANSMISSION ERROR"); } 
    finally { setLoading(false); }
  };

  return (
    <div style={styles.mainWrapper} className="crt-flicker">
      {/* The CRT Overlay Layer */}
      <div className="scanlines"></div>

      <div style={styles.glassPanel}>
        {/* HEADER */}
        <div style={styles.headerContainer}>
          <h1 style={styles.glitchHeader}>
            A L C H E M I S T
          </h1>
          <p style={styles.status}>SYSTEM STATUS: <span style={{color: "#fff"}}>ONLINE</span></p>
        </div>

        {/* CONTROL DECK */}
        <div style={styles.controlDeck}>
          <div style={styles.uploadZone}>
            <label style={styles.fileLabel}>
              {file ? `>> LOADED: ${file.name}` : ">> UPLOAD_SOURCE_IMAGE"}
              <input 
                type="file" 
                onChange={(e) => setFile(e.target.files[0])}
                style={{display: "none"}}
              />
            </label>
          </div>
          
          <button 
            onClick={handleTransmute}
            disabled={loading || !file}
            className="glitch-btn"
            style={styles.actionBtn}
          >
            {loading ? "PROCESSING..." : "EXECUTE_TRANSMUTATION"}
          </button>
        </div>

        {/* OUTPUT TERMINAL */}
        {asciiArt && (
          <div style={styles.terminalWindow}>
            <div style={styles.terminalBar}>/// OUTPUT_STREAM_V1.0</div>
            <pre style={styles.asciiContent}>{asciiArt}</pre>
          </div>
        )}
      </div>

      {/* HISTORY REEL */}
      <div style={styles.historyStrip}>
        {history.map((item, idx) => (
          <div key={idx} style={styles.historyCard}>
            <pre style={styles.miniAscii}>{item.art}</pre>
          </div>
        ))}
      </div>
    </div>
  );
}

const styles = {
  mainWrapper: {
    minHeight: "100vh",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    padding: "20px",
    background: "radial-gradient(circle, #111 0%, #000 100%)",
  },
  glassPanel: {
    background: "rgba(10, 20, 10, 0.6)",
    backdropFilter: "blur(10px)",
    border: "1px solid #333",
    padding: "40px",
    borderRadius: "0px",
    width: "100%",
    maxWidth: "900px",
    boxShadow: "0 0 50px rgba(0, 255, 0, 0.1)",
    position: "relative",
    zIndex: 10,
  },
  headerContainer: {
    borderBottom: "1px solid #333",
    paddingBottom: "20px",
    marginBottom: "30px",
    display: "flex",
    justifyContent: "space-between",
    alignItems: "flex-end",
  },
  glitchHeader: {
    margin: 0,
    fontSize: "3rem",
    letterSpacing: "5px",
    textTransform: "uppercase",
    // Ensure the text wraps if on mobile
    maxWidth: "100%", 
    lineHeight: "1.1",
  },
  status: {
    fontSize: "0.8rem",
    color: "#555",
    margin: 0,
    paddingBottom: "5px", // Align slightly with the large text
  },
  controlDeck: {
    display: "flex",
    gap: "20px",
    marginBottom: "40px",
    flexWrap: "wrap", // Good for responsiveness
  },
  uploadZone: {
    flex: 1,
    minWidth: "200px",
    border: "1px dashed #333",
    padding: "15px",
    cursor: "pointer",
    transition: "0.3s",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
  },
  fileLabel: {
    cursor: "pointer",
    width: "100%",
    textAlign: "center",
  },
  actionBtn: {
    background: "transparent",
    border: "1px solid var(--neon-green)",
    color: "var(--neon-green)",
    padding: "15px 40px",
    fontSize: "1rem",
    cursor: "pointer",
    fontFamily: "inherit",
    fontWeight: "bold",
    minWidth: "200px",
  },
  terminalWindow: {
    background: "#000",
    border: "1px solid #333",
    marginTop: "20px",
  },
  terminalBar: {
    background: "#111",
    padding: "5px 10px",
    fontSize: "0.7rem",
    color: "#666",
    borderBottom: "1px solid #333",
  },
  asciiContent: {
    padding: "20px",
    fontSize: "8px",
    lineHeight: "8px",
    overflowX: "auto",
    color: "#0aff0a",
    margin: 0,
  },
  historyStrip: {
    marginTop: "40px",
    display: "flex",
    gap: "10px",
    width: "100%",
    maxWidth: "900px",
    overflowX: "auto",
    padding: "10px 0",
    zIndex: 10,
    opacity: 0.7,
  },
  historyCard: {
    minWidth: "120px",
    height: "120px",
    background: "#000",
    border: "1px solid #222",
    overflow: "hidden",
    position: "relative",
  },
  miniAscii: {
    fontSize: "2px",
    lineHeight: "2px",
    margin: 0,
    padding: "5px",
  }
};