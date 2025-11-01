#BACKEND
from flask import Flask,render_template,request jsonify  
from flask_cors import CORS #another port frontend running
import backend_logic as backend

app = Flask(__name__)
CORS(app)

print("Starting backend")
#loads data and ml model
backend.load_data()
backend.load_model()

#routes for frontend,responses
    @app.route('/')
    def index():
        return render_template('index.html')
    #accept user input and return response
    @app.route('/api/chat', methods=['POST'])
    def chat():
        data = request.json#reads json body from request
        query=data.get('query','').strip()#extract users qn
        if not query:
            return jsonify({'error': 'No message provided'}), 400
        
        #process query using backend logic
        result=backend.samrath_query(query)

    #query-dictionary
        if isinstance(result, dict) and 'error' in result:
            return jsonify({
                    'success': False,
                    'response': result['error'],
                    'type': 'error'
                }), 500
        
        if result.get('type')='dataframe':
            return jsonify({
                'success': True,
                    'response': result['data'],
                    'type': 'table',
                    'query_type': result.get('query_type', 'unknown')

            })
        
        elif result.get('type') == 'json':
                # Format JSON response as readable text
                data = result['data']
                if isinstance(data, dict):
                    formatted = "\n".join([f"{k.replace('_', ' ').title()}: {v}" for k, v in data.items()])
                    return jsonify({
                        'success': True,
                        'response': formatted,
                        'type': 'text',
                        'query_type': result.get('query_type', 'unknown')
                    })
        return jsonify({
                'success': True,
                'response': result.get('data', str(result)),
                'type': 'text',
                'query_type': result.get('query_type', 'unknown')
            })
            
    except Exception as e:
            print(f"Error processing query: {str(e)}")
            traceback.print_exc()
            return jsonify({
                'success': False,
                'response': f'Sorry, an error occurred: {str(e)}',
                'type': 'error'
            }), 500

    @app.route('/api/examples', methods=['GET'])
    def examples():
        return jsonify({
            'examples': [
                'Compare rainfall in Maharashtra and Kerala for last 5 years',
                'Show top crops in Punjab',
                'Show production trend of Rice in Tamil Nadu',
                'What are the statistics for Karnataka?',
                'Compare monsoon rainfall between Gujarat and Rajasthan'
            ]
        })

if __name__ == '__main__':
    print("🚀 Starting Samarth Q&A Server...")
    print("📡 Server running at http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)