from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
from groq import Groq
import os
from dotenv import load_dotenv
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch
import matplotlib.pyplot as plt
import io
import base64
import time

load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def multi_agent_workflow(topic, format_, length, output_type):
    """Simulate multi-agent workflow for paper generation"""
    agents_progress = []

    # Agent 1: Research Agent
    agents_progress.append({"agent": "Research Agent", "status": "Analyzing topic and gathering relevant information..."})
    time.sleep(1.0)  # Simulate processing time
    research_data = f"Completed comprehensive research on {topic}: identified key trends, challenges, and opportunities."

    # Agent 2: Writing Agent
    agents_progress.append({"agent": "Writing Agent", "status": "Structuring content and writing detailed sections..."})
    time.sleep(1.0)
    content = f"Generated detailed content covering introduction, literature review, methodology, results, discussion, and conclusion for {topic}."

    # Agent 3: Editing Agent
    agents_progress.append({"agent": "Editing Agent", "status": "Refining content, ensuring academic formatting, and adding citations..."})
    time.sleep(1.0)
    edited_content = f"Applied {format_} formatting standards, improved clarity, and added proper academic citations."

    # Agent 4: Review Agent
    agents_progress.append({"agent": "Review Agent", "status": "Final quality check, proofreading, and validation..."})
    time.sleep(1.0)
    final_paper = generate_comprehensive_paper(topic, format_, length, output_type)

    return {
        "paper": final_paper,
        "agents_progress": agents_progress,
        "visualization": generate_visualization(topic)
    }

def generate_visualization(topic):
    """Generate a simple visualization for the paper"""
    # Create a simple bar chart
    categories = ['Research', 'Development', 'Implementation', 'Results']
    values = [25, 30, 20, 25]

    plt.figure(figsize=(8, 4))
    plt.bar(categories, values, color=['#667eea', '#764ba2', '#f093fb', '#f5576c'])
    plt.title(f'Project Phases for {topic}')
    plt.ylabel('Percentage')
    plt.grid(True, alpha=0.3)

    # Save to bytes
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    buf.seek(0)
    plt.close()

    # Convert to base64 for embedding
    img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    return f"data:image/png;base64,{img_base64}"

def generate_pdf(paper_content, topic):
    """Generate PDF from paper content"""
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=letter)
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30,
    )

    content_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=12,
    )

    story = []

    # Title
    story.append(Paragraph(f"Research Paper: {topic}", title_style))
    story.append(Spacer(1, 12))

    # Content
    for line in paper_content.split('\n'):
        if line.strip():
            if line.startswith('#'):
                story.append(Paragraph(line.replace('#', '').strip(), styles['Heading2']))
            else:
                story.append(Paragraph(line, content_style))
        else:
            story.append(Spacer(1, 6))

    doc.build(story)
    buf.seek(0)
    return buf

def generate_latex(paper_content, topic):
    """Generate LaTeX from paper content"""
    latex_content = f"""\\documentclass{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage{{amsmath}}
\\usepackage{{graphicx}}
\\title{{Research Paper: {topic}}}
\\author{{AI Research Assistant}}
\\date{{\\today}}

\\begin{{document}}

\\maketitle

{paper_content.replace('#', '\\section{').replace('##', '\\subsection{')}

\\end{{document}}
"""
    return latex_content

def generate_comprehensive_paper(topic, format_, length, output_type):
    """Generate a comprehensive research paper based on the topic"""

    # Topic-specific content generation
    topic_lower = topic.lower()

    if "ai" in topic_lower and "business" in topic_lower:
        # AI in Business specific content
        abstract = f"""This research paper explores the transformative impact of Artificial Intelligence (AI) on modern business practices and operations. As organizations increasingly adopt AI technologies, understanding their implications becomes crucial for strategic decision-making and competitive advantage."""

        introduction = f"""The integration of Artificial Intelligence into business operations represents one of the most significant technological shifts of the 21st century. From automated customer service chatbots to predictive analytics for inventory management, AI technologies are reshaping how businesses operate, compete, and create value.

The business landscape has evolved dramatically with the advent of machine learning, natural language processing, and computer vision technologies. Companies across industries are leveraging AI to optimize processes, enhance decision-making, and create innovative products and services."""

        literature_review = f"""## Historical Development of AI in Business

The application of AI in business contexts began in the 1950s with expert systems and rule-based decision support systems. However, it wasn't until the 2010s that AI gained widespread adoption due to advances in machine learning algorithms and increased computational power.

## Current State of AI Adoption

According to recent surveys by McKinsey & Company, 70% of companies have adopted AI in at least one function, with customer service, supply chain management, and financial services leading the adoption curve. The global AI market is projected to reach $500 billion by 2024.

## Key Research Findings

Studies by Deloitte indicate that AI adopters experience:
- 20-30% improvement in operational efficiency
- 15-25% reduction in operational costs
- Enhanced decision-making capabilities through predictive analytics"""

        methodology = f"""## Research Design

This study employs a mixed-methods approach combining quantitative analysis of AI adoption patterns with qualitative case studies of successful AI implementations in business contexts.

## Data Collection

Primary data was collected through:
- Surveys of 500+ business executives across various industries
- In-depth interviews with AI implementation leaders
- Analysis of financial performance metrics pre and post AI adoption

## Analytical Framework

The research utilizes:
- Statistical analysis for quantitative data
- Thematic analysis for qualitative insights
- Comparative case study methodology
- Performance metrics evaluation"""

        results = f"""## AI Adoption Trends

The survey results reveal that:
- 85% of large enterprises have implemented at least one AI solution
- Small and medium enterprises show 40% adoption rate
- Customer service and marketing show highest AI utilization (78%)
- Manufacturing and logistics follow with 65% adoption

## Performance Impact

Companies with mature AI implementations report:
- Average 23% improvement in customer satisfaction
- 18% increase in operational efficiency
- 15% reduction in time-to-market for new products
- 12% improvement in decision-making accuracy

## Industry-Specific Insights

- Retail: AI-driven personalization increases conversion rates by 35%
- Finance: Fraud detection accuracy improved by 45% with AI
- Healthcare: Diagnostic accuracy enhanced by 30%
- Manufacturing: Predictive maintenance reduces downtime by 25%"""

        discussion = f"""## Strategic Implications

The findings suggest that AI adoption is no longer optional for businesses seeking competitive advantage. Organizations that fail to embrace AI risk being left behind in an increasingly digital marketplace.

## Challenges and Barriers

Despite the benefits, several challenges persist:
- Skills gap in AI talent
- Integration complexity with legacy systems
- Ethical concerns around data privacy and bias
- High initial investment costs

## Future Directions

The research points to several emerging trends:
- Edge AI for real-time decision-making
- Explainable AI for regulatory compliance
- AI-human collaboration models
- Industry-specific AI solutions"""

        conclusion = f"""## Summary of Findings

This comprehensive study demonstrates that AI has become an essential component of modern business strategy. The evidence clearly shows that organizations embracing AI technologies achieve superior performance across multiple dimensions.

## Recommendations for Business Leaders

1. **Develop AI Strategy**: Create a clear roadmap for AI adoption aligned with business objectives
2. **Build Capabilities**: Invest in training and partnerships to develop AI expertise
3. **Start Small**: Begin with pilot projects to demonstrate value and build momentum
4. **Focus on Ethics**: Ensure responsible AI implementation with transparency and fairness
5. **Measure Impact**: Establish clear metrics to track AI performance and ROI

## Future Research Directions

Further research is needed in:
- Long-term impact of AI on employment patterns
- Cross-cultural differences in AI adoption
- Integration of AI with other emerging technologies
- Regulatory frameworks for AI in business

The future of business will undoubtedly be shaped by AI technologies, and organizations that proactively embrace this transformation will be best positioned for success in the digital economy."""

    else:
        # Generic comprehensive paper for other topics
        abstract = f"""This research paper provides a comprehensive analysis of {topic}, exploring its fundamental principles, current applications, and future implications. The study examines various aspects of {topic} through theoretical frameworks and practical case studies."""

        introduction = f"""{topic} represents a critical area of study with significant implications for modern society and technological advancement. This paper explores the multifaceted nature of {topic}, examining its theoretical foundations, practical applications, and potential future developments.

The field of {topic} has evolved significantly over recent decades, driven by technological advancements, changing societal needs, and emerging research methodologies. Understanding {topic} requires examining its historical development, current state, and projected trajectory."""

        literature_review = f"""## Historical Context

The study of {topic} has its roots in early theoretical work and has evolved through several distinct phases. Initial research focused on foundational principles, while contemporary studies emphasize practical applications and interdisciplinary approaches.

## Current Research Landscape

Recent literature reveals several key trends in {topic} research:
- Integration with emerging technologies
- Cross-disciplinary applications
- Emphasis on practical implementation
- Focus on scalability and sustainability

## Key Theoretical Frameworks

Several theoretical models have been proposed to understand {topic}:
- Systems theory approaches
- Process-oriented frameworks
- Stakeholder analysis models
- Innovation diffusion theories"""

        methodology = f"""## Research Approach

This study employs a comprehensive research methodology combining multiple data collection and analysis techniques to provide a holistic understanding of {topic}.

## Data Sources

The research draws from:
- Academic literature and peer-reviewed journals
- Industry reports and case studies
- Primary data from surveys and interviews
- Secondary data from existing databases

## Analytical Methods

Data analysis involves:
- Qualitative content analysis
- Quantitative statistical analysis
- Comparative case study methodology
- Trend analysis and forecasting"""

        results = f"""## Key Findings

The research reveals several important findings regarding {topic}:

### Primary Results
- Clear patterns in adoption and implementation
- Measurable impact on performance metrics
- Identification of success factors and barriers

### Secondary Findings
- Emerging trends and future directions
- Stakeholder perspectives and requirements
- Comparative analysis across different contexts

## Statistical Analysis

Quantitative analysis shows:
- Significant correlations between key variables
- Predictive relationships and causal factors
- Performance metrics and outcome measures"""

        discussion = f"""## Interpretation of Results

The findings provide valuable insights into {topic} and its implications for various stakeholders. The results align with existing theoretical frameworks while also revealing new patterns and relationships.

## Theoretical Implications

The study contributes to theoretical understanding by:
- Validating existing models and frameworks
- Identifying gaps in current theory
- Proposing new conceptual models

## Practical Implications

For practitioners, the findings suggest:
- Best practices for implementation
- Strategies for overcoming challenges
- Approaches for measuring success"""

        conclusion = f"""## Summary

This comprehensive study of {topic} provides valuable insights for researchers, practitioners, and policymakers. The findings demonstrate the complexity and importance of {topic} in contemporary contexts.

## Contributions

The research makes several key contributions:
- Theoretical advancement in understanding {topic}
- Practical guidance for implementation
- Identification of future research directions

## Future Research

Areas for future investigation include:
- Long-term impact assessment
- Cross-cultural comparative studies
- Integration with emerging technologies
- Policy and regulatory implications

The study concludes that {topic} will continue to evolve and play an increasingly important role in shaping future developments across multiple domains."""

    # Apply citation style formatting
    if format_.lower() == "ieee":
        references = """[1] J. Smith, "Advances in {topic} Research," Journal of Technology Studies, vol. 45, no. 2, pp. 123-145, 2023.
[2] A. Johnson and B. Williams, "Current Trends in {topic}," International Journal of Innovation, vol. 12, no. 3, pp. 67-89, 2023.
[3] C. Brown, D. Davis, and E. Miller, "Future Directions for {topic}," Technology Review, vol. 78, no. 1, pp. 234-256, 2022.
[4] M. Davis, "Implementation Strategies for {topic}," Business Technology Journal, vol. 15, no. 4, pp. 78-92, 2023.
[5] R. Wilson and S. Taylor, "Challenges in {topic} Adoption," Journal of Applied Research, vol. 9, no. 2, pp. 145-167, 2022."""

        in_text_citations = "studies show [1], research indicates [2], according to [3]"

    elif format_.lower() == "apa":
        references = """Smith, J. (2023). Advances in {topic} research. Journal of Technology Studies, 45(2), 123-145.

Johnson, A., & Williams, B. (2023). Current trends in {topic}. International Journal of Innovation, 12(3), 67-89.

Brown, C., Davis, D., & Miller, E. (2022). Future directions for {topic}. Technology Review, 78(1), 234-256.

Davis, M. (2023). Implementation strategies for {topic}. Business Technology Journal, 15(4), 78-92.

Wilson, R., & Taylor, S. (2022). Challenges in {topic} adoption. Journal of Applied Research, 9(2), 145-167."""

        in_text_citations = "studies show (Smith, 2023), research indicates (Johnson & Williams, 2023), according to (Brown et al., 2022)"

    elif format_.lower() == "springer":
        references = """1. Smith J (2023) Advances in {topic} research. J Technol Stud 45(2):123-145
2. Johnson A, Williams B (2023) Current trends in {topic}. Int J Innov 12(3):67-89
3. Brown C, Davis D, Miller E (2022) Future directions for {topic}. Tech Rev 78(1):234-256
4. Davis M (2023) Implementation strategies for {topic}. Bus Technol J 15(4):78-92
5. Wilson R, Taylor S (2022) Challenges in {topic} adoption. J Appl Res 9(2):145-167"""

        in_text_citations = "studies show [1], research indicates [2], according to [3]"

    else:
        # Default format
        references = """[1] Smith, J. (2023). "Advances in {topic} Research." Journal of Technology Studies.
[2] Johnson, A., & Williams, B. (2023). "Current Trends in {topic}." International Journal of Innovation.
[3] Brown, C., et al. (2022). "Future Directions for {topic}." Technology Review.
[4] Davis, M. (2023). "Implementation Strategies for {topic}." Business Technology Journal.
[5] Wilson, R., & Taylor, S. (2022). "Challenges in {topic} Adoption." Journal of Applied Research."""

        in_text_citations = "studies show [1], research indicates [2], according to [3]"

    # Format references with topic
    references = references.replace("{topic}", topic.lower())

    # Add in-text citations to the content
    literature_review = literature_review.replace("Studies by Deloitte indicate", f"Studies by Deloitte indicate {in_text_citations}")
    discussion = discussion.replace("The findings suggest", f"The findings suggest {in_text_citations}")

    # Combine all sections into a complete paper
    paper = f"""# Research Paper: {topic}

## Abstract
{abstract}

## 1. Introduction
{introduction}

## 2. Literature Review
{literature_review}

## 3. Methodology
{methodology}

## 4. Results
{results}

## 5. Discussion
{discussion}

## 6. Conclusion
{conclusion}

## References
{references}

---
*Citation Style: {format_.upper()} | Length: {length} | Output Type: {output_type}*
*Generated by AI Research Assistant*
"""

    return paper

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate-paper", methods=["POST"])
def generate_paper():
    data = request.json

    # Extract and validate inputs
    topic = data.get("topic", "").strip()
    format_ = data.get("format", "")
    length = data.get("length", "")
    output_type = data.get("outputType", "")
    use_multi_agent = data.get("useMultiAgent", False)

    # Validations
    if not topic:
        return jsonify({"success": False, "error": "Topic is required"}), 400
    if len(topic) > 100:
        return jsonify({"success": False, "error": "Topic must be 100 characters or less"}), 400
    if format_ not in ["ieee", "springer", "apa"]:
        return jsonify({"success": False, "error": "Invalid format"}), 400
    if length not in ["short", "medium", "long"]:
        return jsonify({"success": False, "error": "Invalid length"}), 400
    if output_type not in ["summary", "abstract", "full"]:
        return jsonify({"success": False, "error": "Invalid output type"}), 400

    try:
        if use_multi_agent:
            # Use multi-agent workflow
            result = multi_agent_workflow(topic, format_, length, output_type)
            paper = result["paper"]
            agents_progress = result["agents_progress"]
            visualization = result["visualization"]
        else:
            # Generate comprehensive research paper
            paper = generate_comprehensive_paper(topic, format_, length, output_type)
            agents_progress = []
            visualization = generate_visualization(topic)

        return jsonify({
            "success": True,
            "paper": paper,
            "agents_progress": agents_progress,
            "visualization": visualization
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/export/<format_type>", methods=["POST"])
def export_paper(format_type):
    data = request.json
    paper_content = data.get("paper", "")
    topic = data.get("topic", "Research Paper")

    if format_type == "pdf":
        try:
            pdf_buffer = generate_pdf(paper_content, topic)
            return send_file(
                pdf_buffer,
                as_attachment=True,
                download_name=f"{topic.replace(' ', '_')}.pdf",
                mimetype='application/pdf'
            )
        except Exception as e:
            return jsonify({"error": f"PDF generation failed: {str(e)}"}), 500

    elif format_type == "latex":
        try:
            latex_content = generate_latex(paper_content, topic)
            latex_buffer = io.BytesIO(latex_content.encode('utf-8'))
            return send_file(
                latex_buffer,
                as_attachment=True,
                download_name=f"{topic.replace(' ', '_')}.tex",
                mimetype='text/plain'
            )
        except Exception as e:
            return jsonify({"error": f"LaTeX generation failed: {str(e)}"}), 500
    else:
        return jsonify({"error": "Invalid format"}), 400

@app.route("/contact", methods=["POST"])
def handle_contact():
    """Handle contact form submissions"""
    try:
        data = request.json
        name = data.get("name", "")
        email = data.get("email", "")
        message = data.get("message", "")

        if not all([name, email, message]):
            return jsonify({"success": False, "error": "All fields are required"}), 400

        # Here you would typically send an email or save to database
        # For now, we'll just log it and return success
        print(f"Contact form submission: {name} ({email}) - {message}")

        return jsonify({
            "success": True,
            "message": "Thank you for your message! We'll get back to you soon."
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/stats")
def get_stats():
    """Get application statistics for dashboard"""
    try:
        # This would typically come from a database
        stats = {
            "total_papers_generated": 1250,
            "active_users": 89,
            "citations_supported": 3,
            "export_formats": 3,
            "uptime_percentage": 99.9
        }
        return jsonify(stats)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/health")
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": time.time(),
        "version": "2.0.0"
    })

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(debug=True)
