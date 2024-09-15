class Rangerchat < Formula
    desc "A command-line tool to interact with OpenAI's GPT-4 model"
    homepage "https://github.com/davidtkeane/rangerchat.git"
    url "https://github.com/davidtkeane/rangerchat/archive/refs/tags/v0.1.0.tar.gz"
    sha256 "126406ea5dda23858e1945e75139d1f025566a56048e7d35759a97bd1db8e91c"
    license "MIT"
  
    depends_on "python@3.10"  # Or whatever Python version your project requires
  
    def install
      # Install Python dependencies
      system "pip3", "install", "-r", "requirements.txt"
  
      # Install the script
      bin.install "rgpt.py" => "rgpt"
    end
  
    test do
      # Test the formula (optional)
      system "#{bin}/rgpt", "--help"
    end
  end
  