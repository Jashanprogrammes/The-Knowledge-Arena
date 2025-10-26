#!/usr/bin/env python3
"""
Quiz Royale Footer Customization Script
=======================================

This script helps you easily update the footer with your actual team information.
Just run this script and follow the prompts to customize your footer!

Usage:
    python update_footer.py
"""

def get_team_info():
    """Get team information from user input"""
    print("🏆 QUIZ ROYALE FOOTER CUSTOMIZATION 🏆")
    print("=" * 50)
    
    # Get team members
    team_members = []
    print("\n👨‍💻 TEAM MEMBERS:")
    print("Enter your team members (press Enter with empty name to finish):")
    
    member_count = 1
    while True:
        name = input(f"Developer {member_count} Name: ").strip()
        if not name:
            break
        
        uid = input(f"Developer {member_count} UID: ").strip()
        if not uid:
            uid = "Not provided"
        
        team_members.append({"name": name, "uid": uid})
        member_count += 1
    
    # Get mentor information
    print("\n🎓 MENTOR INFORMATION:")
    mentor_name = input("Mentor Name: ").strip() or "Mentor Name"
    mentor_email = input("Mentor Email: ").strip() or "mentor@example.com"
    institution = input("Institution Name: ").strip() or "Institution Name"
    
    # Get project information
    print("\n🚀 PROJECT INFORMATION:")
    dev_period = input("Development Period (e.g., 2024): ").strip() or "2024"
    tech_stack = input("Technology Stack: ").strip() or "Python, Streamlit, HTML/CSS, JSON"
    
    return {
        "team_members": team_members,
        "mentor": {
            "name": mentor_name,
            "email": mentor_email,
            "institution": institution
        },
        "project": {
            "period": dev_period,
            "tech_stack": tech_stack
        }
    }

def generate_footer_code(team_info):
    """Generate the footer code with team information"""
    
    # Generate team members HTML
    team_members_html = ""
    for member in team_info["team_members"]:
        team_members_html += f'                    <p style="font-family: \'Inter\', sans-serif; font-size: 1.1em; margin: 5px 0; color: white;">🎮 {member["name"]} - UID: {member["uid"]}</p>\n'
    
    # Generate the complete footer code
    footer_code = f'''def render_footer():
    """Render the team footer"""
    st.markdown("""
    <div style="margin-top: 50px; padding: 30px; background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%); border-radius: 20px; backdrop-filter: blur(10px); border: 2px solid rgba(255,255,255,0.1); position: relative; overflow: hidden;">
        <div style="position: absolute; top: -50%; left: -50%; width: 200%; height: 200%; background: conic-gradient(transparent, rgba(255,255,255,0.05), transparent); animation: rotate 15s linear infinite; opacity: 0.3;"></div>
        
        <div style="text-align: center; position: relative; z-index: 1;">
            <h3 style="font-family: 'Orbitron', monospace; font-size: 1.8em; margin-bottom: 20px; background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-shadow: 0 0 20px rgba(255, 255, 255, 0.3);">🏆 QUIZ ROYALE DEVELOPMENT TEAM 🏆</h3>
            
            <div style="display: flex; justify-content: center; flex-wrap: wrap; gap: 30px; margin-bottom: 25px;">
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; padding: 20px; min-width: 200px; box-shadow: 0 8px 16px rgba(0,0,0,0.3); border: 2px solid rgba(255,255,255,0.1);">
                    <h4 style="font-family: 'Poppins', sans-serif; font-size: 1.3em; margin-bottom: 10px; color: #feca57;">👨‍💻 Team Members</h4>
{team_members_html.rstrip()}
                </div>
                
                <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); border-radius: 15px; padding: 20px; min-width: 200px; box-shadow: 0 8px 16px rgba(0,0,0,0.3); border: 2px solid rgba(255,255,255,0.1);">
                    <h4 style="font-family: 'Poppins', sans-serif; font-size: 1.3em; margin-bottom: 10px; color: #feca57;">🎓 Mentor</h4>
                    <p style="font-family: 'Inter', sans-serif; font-size: 1.1em; margin: 5px 0; color: white;">👨‍🏫 {team_info["mentor"]["name"]}</p>
                    <p style="font-family: 'Inter', sans-serif; font-size: 1.1em; margin: 5px 0; color: white;">📧 {team_info["mentor"]["email"]}</p>
                    <p style="font-family: 'Inter', sans-serif; font-size: 1.1em; margin: 5px 0; color: white;">🏢 {team_info["mentor"]["institution"]}</p>
                </div>
            </div>
            
            <div style="background: linear-gradient(135deg, #45b7d1 0%, #96ceb4 100%); border-radius: 15px; padding: 20px; margin-top: 20px; box-shadow: 0 8px 16px rgba(0,0,0,0.3); border: 2px solid rgba(255,255,255,0.1);">
                <h4 style="font-family: 'Poppins', sans-serif; font-size: 1.3em; margin-bottom: 15px; color: #feca57;">🚀 Project Information</h4>
                <p style="font-family: 'Inter', sans-serif; font-size: 1.1em; margin: 8px 0; color: white;">📅 Development Period: {team_info["project"]["period"]}</p>
                <p style="font-family: 'Inter', sans-serif; font-size: 1.1em; margin: 8px 0; color: white;">🛠️ Technology Stack: {team_info["project"]["tech_stack"]}</p>
                <p style="font-family: 'Inter', sans-serif; font-size: 1.1em; margin: 8px 0; color: white;">🎯 Project Type: Interactive Quiz Game</p>
                <p style="font-family: 'Inter', sans-serif; font-size: 1.1em; margin: 8px 0; color: white;">💡 Special Thanks: Our amazing mentor for guidance and support!</p>
            </div>
            
            <div style="margin-top: 20px; padding-top: 20px; border-top: 2px solid rgba(255,255,255,0.2);">
                <p style="font-family: 'Inter', sans-serif; font-size: 1em; color: rgba(255,255,255,0.8); margin: 0;">Made with ❤️ by our amazing development team | © {team_info["project"]["period"]} Quiz Royale</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)'''
    
    return footer_code

def main():
    """Main function"""
    try:
        # Get team information
        team_info = get_team_info()
        
        # Generate footer code
        footer_code = generate_footer_code(team_info)
        
        # Save to file
        with open("footer_code.txt", "w", encoding="utf-8") as f:
            f.write(footer_code)
        
        print("\n✅ SUCCESS!")
        print("=" * 30)
        print("Your customized footer code has been saved to 'footer_code.txt'")
        print("\nTo update your Quiz Royale footer:")
        print("1. Open quiz_royale.py")
        print("2. Find the 'render_footer()' function")
        print("3. Replace it with the code from 'footer_code.txt'")
        print("4. Save and run your game!")
        
        print(f"\n📊 SUMMARY:")
        print(f"Team Members: {len(team_info['team_members'])}")
        print(f"Mentor: {team_info['mentor']['name']}")
        print(f"Institution: {team_info['mentor']['institution']}")
        
    except KeyboardInterrupt:
        print("\n\n❌ Operation cancelled by user.")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
