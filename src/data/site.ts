// ─────────────────────────────────────────────────────────────────────────────
// SINGLE SOURCE OF TRUTH FOR ALL SITE CONTENT
// Edit this file to change the site. You never need to touch layout files.
// Lines marked  // TODO  are placeholders waiting on your input.
// ─────────────────────────────────────────────────────────────────────────────

export const profile = {
  name: "H M Taseen Jubair Bhuiyan",
  shortName: "T. J. Bhuiyan",
  // The eyebrow line above the hero heading.
  kicker: "Public Health · Data · Research",
  // Shown under the name in the sidebar. Keep to ~10 words.
  role: "Public Health & Development Research",
  location: "Dhaka, Bangladesh", // TODO confirm
  // Sidebar bio: 2 to 3 short lines.
  bio: "Research associate working across public health, WASH, and disaster resilience, turning field data into evidence for planning and policy.", // TODO confirm
  // Put your photo in  public/assets/  and set the filename here.
  // Leave as null and the site renders your initials instead.
  photo: null as string | null, // e.g. "assets/taseen.jpg"
  photoAlt: "Portrait of H M Taseen Jubair Bhuiyan",
  // Resume/CV PDF in  public/assets/ . Leave null to hide the download button.
  resume: null as string | null, // e.g. "assets/taseen-jubair-cv.pdf"
};

export const socials = [
  { label: "Email", href: "mailto:taseenjubair@gmail.com", icon: "mail" },
  { label: "LinkedIn", href: "https://www.linkedin.com/in/hmtaseenjubair/", icon: "linkedin" },
  {
    label: "ResearchGate",
    href: "https://www.researchgate.net/profile/Hm-Taseen-Jubair-Bhuiyan",
    icon: "researchgate",
  },
  { label: "ORCID", href: "https://orcid.org/0009-0000-7525-1208", icon: "orcid" },
  { label: "GitHub", href: "https://github.com/tj8868", icon: "github" }, // TODO confirm
];

export const nav = [
  { label: "About", href: "/" },
  { label: "Publications", href: "/publications/" },
  { label: "Experience", href: "/experience/" },
  { label: "CV", href: "/cv/" },
];

export const stats = [
  { value: "3+", label: "Published research papers", note: "incl. Elsevier & Scopus-indexed" },
  { value: "3", label: "Works currently under review" },
  { value: "4+", label: "Years field & research experience" },
  { value: "2", label: "Active research roles", note: "2026" },
];

export const about = {
  lead: "Public health and development research professional with experience supporting healthcare, WASH, and disaster resilience projects through data-driven analysis, field coordination, and technical reporting.",
  sections: [
    {
      heading: "Background",
      paragraphs: [
        "I began in civil engineering at RUET and moved toward public health and development research, where infrastructure, environment, and population health intersect. That path now runs through an M.Sc. in Applied Statistics and Data Science at Jahangirnagar University.",
        "My work sits between the field and the analysis: designing collection instruments, running KIIs and FGDs, validating what comes back, and turning it into something a planner or a policymaker can act on.",
      ],
    },
    {
      heading: "Current work",
      paragraphs: [
        "At Daffodil International University I support public health research on healthcare data analysis, disease patterns, and health monitoring systems, from study design through statistical interpretation and reporting.",
        "Recent work with the Cox's Bazar Development Authority covered WASH infrastructure and cyclone shelter assessments, with GIS-based vulnerability and risk mapping feeding directly into emergency response strategy.",
      ],
    },
  ],
  interests: [
    "Public Health Research",
    "WASH & Environmental Health",
    "Disaster Risk Reduction",
    "Geospatial Vulnerability Analysis",
    "Applied Statistics",
    "AI in Health Prediction",
  ],
};

export const skills = [
  {
    group: "Field & Program",
    items: [
      "Field Coordination",
      "Stakeholder Engagement",
      "Program Monitoring",
      "WASH Assessment",
      "KII / FGD",
      "DRR Frameworks",
    ],
  },
  {
    group: "Data Collection",
    items: [
      "KoboToolbox",
      "GPS Survey",
      "Structured Surveys",
      "Data Validation",
      "Quality Assurance",
    ],
  },
  {
    group: "Analysis & GIS",
    items: [
      "ArcGIS Pro",
      "QGIS",
      "Vulnerability Mapping",
      "Risk Mapping",
      "Statistical Analysis",
    ],
  },
  {
    group: "Programming & Data",
    items: ["Python", "Pandas", "NumPy", "scikit-learn", "R", "SQL", "Microsoft Excel"],
  },
  {
    group: "Reporting & Communication",
    items: [
      "Technical Report Writing",
      "Research Documentation",
      "Evidence-based Planning",
      "Policy Briefs",
    ],
  },
];

export const experience = [
  {
    period: "Jul 2026 – Present",
    current: true,
    role: "Sr. Assistant Coordinator",
    org: "Daffodil International University", // TODO confirm employer
    unit: "Health and Development Department",
    points: [
      "Build analysis workflows that turn raw data into findings, using machine learning algorithms in scikit-learn",
      "Develop and maintain the department website",
      "Prepare and deliver presentations of results to departmental and external audiences",
    ],
  },
  {
    period: "Mar 2025 – Present",
    current: true,
    role: "Research Associate",
    org: "Daffodil International University",
    unit: "Department of Public Health",
    points: [
      "Ongoing appointment supporting public health research on healthcare data analysis, disease patterns, and health monitoring systems",
      "Delivered research design, data collection, cleaning, validation, and dataset preparation for analytical studies",
      "Carried out statistical analysis and interpretation of findings for healthcare and public health outputs",
      "Produced technical reports, documentation, and literature summaries with interdisciplinary teams",
    ],
  },
  {
    period: "Nov 2024 – Apr 2025",
    role: "Research Associate",
    org: "Cox's Bazar Development Authority (CoxDA)",
    unit: "Cox's Bazar Masterplan Project",
    points: [
      "Field assessments of WASH infrastructure, cyclone shelters, and disaster-affected communities using KIIs and FGDs",
      "Data collection, validation, and analysis for environmental health and disaster resilience planning",
      "Vulnerability assessment and risk mapping using GIS to support emergency response strategies",
      "Coordinated with government officials, NGO partners, and research teams during field operations",
      "Stakeholder presentation of earthquake and landslide vulnerability analysis findings",
    ],
  },
  {
    period: "Dec 2022 – Aug 2024",
    role: "Lecturer",
    org: "Mymensingh Engineering College",
    unit: "Department of Civil Engineering",
    points: [
      "Delivered applied instruction in engineering subjects with emphasis on fieldwork and analytical problem-solving",
      "Supervised student projects on infrastructure, water systems, and sustainability",
      "Coordinated academic activities and maintained structured documentation",
    ],
  },
  {
    period: "Jun 2022 – Nov 2022",
    role: "Assistant Engineer",
    org: "Daffodil International University",
    unit: "Planning & Development",
    points: [
      "Coordinated project implementation across technical teams, contractors, and administrative stakeholders",
      "Supported project planning, scheduling, documentation, and progress monitoring",
      "Prepared technical reports and progress updates for management",
    ],
  },
];

export type PubStatus = "published" | "review" | "prep";

export const publications: {
  status: PubStatus;
  title: string;
  authors: string;
  venue: string;
  year: string;
  tags: string[];
  href?: string;
}[] = [
  {
    status: "published",
    title:
      "Deciphering the source of heavy metals in industrially affected river sediment of Shitalakshya River, Bangladesh",
    authors: "Jolly, Y.N., Rakib, M.R.J., Kumar, R., … Bhuiyan, T.J. et al.",
    venue: "Journal of Hazardous Materials Advances (Elsevier) · Vol. 10, 100268",
    year: "2023",
    tags: ["Heavy Metals", "River Sediment", "Pollution Source"],
    href: undefined, // TODO add DOI link
  },
  {
    status: "published",
    title:
      "Seasonal and spatial distribution of heavy metals in an industrially affected river: ecological risk, health risk & pollution source",
    authors: "Jolly, Y. et al. [incl. Bhuiyan, T.J.]",
    venue: "Scopus-indexed",
    year: "2023",
    tags: ["Ecological Risk", "Health Risk", "Water Quality"],
    href: undefined, // TODO add DOI link
  },
  {
    status: "published",
    title: "Investigation on the use of demolished concrete and glass in concrete",
    authors: "Bhuiyan, T.J. et al. [First Author]",
    venue: "Landscape Architecture & Regional Planning · Vol. 4(4), pp. 81–86",
    year: "2019",
    tags: ["Sustainable Materials", "Recycled Aggregate"],
    href: undefined, // TODO add DOI link
  },
  {
    status: "review",
    title: "Scoping review on myocardial infarction prediction using artificial intelligence",
    authors: "Bhuiyan, T.J. et al.",
    venue: "Submitted for peer review",
    year: "",
    tags: ["Artificial Intelligence", "Cardiology", "Scoping Review"],
  },
  {
    status: "review",
    title:
      "Multi-metric seismic vulnerability assessment of health facilities in Cox's Bazar, Bangladesh",
    authors: "Bhuiyan, T.J. et al.",
    venue: "Submitted for review",
    year: "",
    tags: ["Seismic Risk", "Health Facilities", "GIS"],
  },
  {
    status: "prep",
    title: "Scoping review on Alzheimer's disease prediction using AI-based approaches",
    authors: "Bhuiyan, T.J. et al.",
    venue: "Manuscript under preparation",
    year: "",
    tags: ["Artificial Intelligence", "Neurology", "Scoping Review"],
  },
];

export const statusLabels: Record<PubStatus, string> = {
  published: "Published",
  review: "Under review",
  prep: "In preparation",
};

export const education = [
  {
    degree: "M.Sc. Applied Statistics & Data Science",
    school: "Jahangirnagar University, Dhaka",
    note: "Thesis programme",
    year: "Expected 2026",
  },
  {
    degree: "B.Sc. Civil Engineering",
    school: "Rajshahi University of Engineering & Technology (RUET)",
    note: null,
    year: "2021",
  },
  {
    degree: "Higher Secondary Certificate",
    school: "Notre Dame College, Dhaka",
    note: null,
    year: "2013",
  },
];

export const contact = {
  blurb:
    "Open to research collaborations, consulting engagements, and full-time opportunities in public health, development research, and data analysis.",
};
