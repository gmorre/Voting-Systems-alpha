from turtle import pd
import pandas as pd
from votekit.graphs import PairwiseComparisonGraph
from votekit.elections import Plurality, IRV
from votekit.utils import score_dict_from_score_vector
from votekit.pref_profile import RankProfile
from votekit.utils import borda_scores
from votekit.elections import Approval
from votekit.utils import score_profile_from_ballot_scores

# copeland method

def copeland_score(profile):
    # Computes the Copeland score for each candidate in the given preference profile.
    pwc_graph = PairwiseComparisonGraph(profile)
    candidate_scores = {candidate: 0 for candidate in profile.candidates}

    for (cand1, cand2), (cand1_wins, cand2_wins) in pwc_graph.pairwise_dict.items():
        if cand1_wins > cand2_wins:
            candidate_scores[cand1] += 1
        elif cand2_wins > cand1_wins:
            candidate_scores[cand2] += 1
        else:  # tie
            candidate_scores[cand1] += 0.5
            candidate_scores[cand2] += 0.5

    return candidate_scores

def copeland_winner(profile):
    #Determines the winner(s) of the Copeland election for the given preference profile.
    scores = copeland_score(profile)
    max_score = max(scores.values())
    winners = [candidate for candidate, score in scores.items() if score == max_score]
    return winners

def copeland_results(profile):
        #prints the results of the Copeland election for the given profile
        copeland_winners = copeland_winner(profile)
        if len(copeland_winners) == 1:
            print("Candidate", copeland_winners[0], "won the election with a Copeland score of", copeland_score(profile)[copeland_winners[0]])
        else:
            print("There is a tie between candidates:", copeland_winners, "with a Copeland score of", copeland_score(profile)[copeland_winners[0]])

# plurality method

def plurality_results(profile):
    election = Plurality(profile=profile, m=1)

    print()
    y=election.election_states[0].scores
    print("Vote Totals")
    for candidate in y:
        print(candidate, int(y[candidate]))
    print()
    total=0
    for candidate in y:
        total=total+y[candidate]
    for candidate in y:
        print("Candidate ", candidate, "received ", round(y[candidate]/total*100,2), "% of the vote.")
    x=0
    winner='none'
    for candidate in y:
        if y[candidate]/total*100 > x:
            x = y[candidate]/total*100  
            winner = candidate
    print()
    print("Candidate", winner, "won the election with ", round(x,2), "% of the vote.")

# IRV

def IRV_results_complete(profile):
    #Prints the results of the IRV election for the given profile, including each round of elimination and the final winner. This function is specifically designed to handle the case when ballots are complete.
    election = IRV(profile=profile)

    for i in range(0, len(election.election_states)-1, 1):
        print("Round ", i + 1, " of the IRV election")
        print()
        x=election.election_states[i].eliminated
        if i>0:
            print("Candidate",iter(x[0]).__next__(), "was eliminated in this round.")
        y=election.election_states[i].scores
        total=0
        for candidate in y:
            total=total+y[candidate]
        print()
        print("Vote Totals")
        for candidate in y:
            print(candidate, int(y[candidate]))
        print()
        print('Total Votes:', total)
        print()
        for candidate in y:
            print("Candidate", candidate, "received ", round(y[candidate]/total*100,2), "% of the vote.")
        for candidate in y:
            if y[candidate]/total*100 > 50:
                print()
                print("Candidate", candidate, "received a majority of the votes and won the election.")
                break
        else:
            print()
            print("No candidate has a majority. We must continue tabulating results to find winner.")
            print()

def IRV_results_undervotes(profile):
    #Prints the results of the IRV election for the given profile, including each round of elimination and the final winner. This function is specifically designed to handle cases where all votes are undervotes (i.e., ballots that that have less than the maximum possible length rankings.).
    election = IRV(profile=profile)

    for i in range(0, len(election.election_states)-2, 1):
        print("Round ", i + 1, " of the IRV election")
        print()
        x=election.election_states[i].eliminated
        if i>0:
            print("Candidate",iter(x[0]).__next__(), "was eliminated in this round.")
        y=election.election_states[i].scores
        total=0
        for candidate in y:
            total=total+y[candidate]
        print()
        print("Vote Totals")
        for candidate in y:
            print(candidate, int(y[candidate]))
        print()
        print('Total Votes:', total)
        print()
        for candidate in y:
            print("Candidate", candidate, "received ", round(y[candidate]/total*100,2), "% of the vote.")
        for candidate in y:
            if y[candidate]/total*100 > 50:
                print()
                print("Candidate", candidate, "received a majority of the votes and won the election.")
                break
        else:
            print()
            print("No candidate has a majority. We must continue tabulating results to find winner.")
            print()

# condorcet

def condorcet_criteria_test_plurality(profile):
    #Tests plurality voting against the Condorcet criterion.
    pwc_graph = PairwiseComparisonGraph(profile)
    p = Plurality(profile=profile, m=1).get_elected()[0]
    plurality_winner,=p

    if pwc_graph.has_condorcet_winner() == True:
        condorcet_winner = pwc_graph.get_condorcet_winner()
        print("The plurality winner is:", plurality_winner)
        print("The Condorcet candidate is:", condorcet_winner)
        if condorcet_winner==plurality_winner:
            print("This election does not violate the Condorcet criterion. The Condorcet candidate is the plurality winner.")
        elif condorcet_winner!=plurality_winner:
            print("This election violates the Condorcet criterion. The Condorcet candidate is NOT the plurality winner.")
    else:
        print("The plurality winner is:", plurality_winner)
        print("There is no Condorcet candidate.")
        print("The election does not violate the Condorcet criterion. There is no Condorcet candidate.")

def condorcet_criteria_test_IRV(profile):
    #Tests IRV against the Condorcet criterion.
    pwc_graph = PairwiseComparisonGraph(profile)
    r = IRV(profile=profile).get_elected()[0]
    irv_winner,=r

    if pwc_graph.has_condorcet_winner() == True:
        condorcet_winner = pwc_graph.get_condorcet_winner()
        print("The IRV winner is:", irv_winner)
        print("The Condorcet candidate is:", condorcet_winner)
        if condorcet_winner==irv_winner:
            print("This election does not violate the Condorcet criterion. The Condorcet candidate is the IRV winner.")
        elif condorcet_winner!=irv_winner:
            print("This election violates the Condorcet criterion. The Condorcet candidate is NOT the IRV winner.")
    else:
        print("The IRV winner is:", irv_winner)
        print("There is no Condorcet candidate.")
        print("The election does not violate the Condorcet criterion. There is no Condorcet candidate.")

def condorcet_criteria_question_IRV(profile):
    #Asks whether IRV violates the Condorcet criterion.
    while True:
        answer = input("Did the IRV election violate the Condorcet criterion? (y/n): ")
        if answer == 'y' or answer == 'n':
            break
        else:
            print("Invalid input")
    pwc_graph = PairwiseComparisonGraph(profile)
    r = IRV(profile=profile).get_elected()[0]
    irv_winner,=r

    if pwc_graph.has_condorcet_winner() == True:
        condorcet_winner = pwc_graph.get_condorcet_winner()
        print("Answer: ",answer)
        print("The IRV winner is:", irv_winner)
        print("The Condorcet candidate is:", condorcet_winner)
        if condorcet_winner==irv_winner:
            if answer == "n":
                print("Correct. The IRV election did not violate the Condorcet criterion.")
            else:
                print("Incorrect. The IRV election did not violate the Condorcet criterion.")
        elif condorcet_winner!=irv_winner:
            if answer == "y":
                print("Correct. The IRV election violated the Condorcet criterion.")
            else:
                print("Incorrect. The IRV election violated the Condorcet criterion.")  
    else:
        print("Answer: ",answer)
        print("The IRV winner is:", irv_winner)
        print("There is no Condorcet candidate.")
        if answer == "n":
            print("Correct. The IRV election did not violate the Condorcet criterion.")
        else:
            print("Incorrect. The IRV election did not violate the Condorcet criterion.") 

#borda method

def n_choice_votes(profile, n):
    """
    Computes nth choice votes for all candidates_cast in a ``RankProfile``.

    Args:
        profile (RankProfile): The profile to compute nth choice votes for.
        n (int): The choice level to compute votes for.

    Returns:
        dict[str, float]:
            Dictionary mapping candidates to number of nth choice votes.
    """
    nchoice = {}
    for candidate in profile.candidates:
        nchoice[candidate] = 0

    for ballot in profile.ballots:
            if len(ballot.ranking) >= n:
                n_place_candidates = ballot.ranking[n - 1]
                weight_per_candidate = ballot.weight / len(n_place_candidates)
                for candidate in n_place_candidates:
                    nchoice[candidate] += weight_per_candidate

    return nchoice


def borda_candidate_score(profile, candidate):
    r"""
    Shows the computation of the Borda score for a specific candidate.
    """
    if candidate not in profile.candidates:
        raise ValueError(f"{candidate!r} is not a candidate in the profile.")

    score = 0
    k = profile.max_ranking_length

    print(f"Candidate {candidate!r} received:")

    for rank in range(1, k + 1):
        votes = n_choice_votes(profile, rank).get(candidate, 0)
        points_per_vote = k - rank+1
        points = votes * points_per_vote

        print(
            f"{votes} votes at rank {rank}, "
            f"resulting in {votes} × {points_per_vote} = {points} points"
        )

        score += points

    print(f"Total Borda score: {score}")

def borda_results(profile):
    # Returns list of winners of Borda election.
    scores = borda_scores(profile)
    max_score = max(scores.values())
    winners = [candidate for candidate, score in scores.items() if score == max_score]
    return winners

def majority_test(profile):
    election = Plurality(profile=profile, m=1)
    y=election.election_states[0].scores

    total=0
    for candidate in y:
        total=total+y[candidate]
    for candidate in y:
        if y[candidate]/total > 0.5:
            m = candidate
            return m  
        else:
            m = None


# approval method

def approval_results(profile):
    # Returns list of winners of Approval election.
    scores = score_profile_from_ballot_scores(profile)
    max_score = max(scores.values())
    winners = [candidate for candidate, score in scores.items() if score == max_score]
    return winners

def approval_details(profile):
    # prints detials of approval election vote totals
    for cand in profile.candidates:
        cand_score_list = []
        ballot_index = 0
        for ballot in profile.ballots:
            if ballot.scores is None:
                raise TypeError(f"Ballot {ballot} has no scores.")
            else:
                if cand in ballot.scores:
                    cand_score_list = cand_score_list + [(ballot.weight,ballot_index)]
                else: 
                    cand_score_list = cand_score_list
            ballot_index = ballot_index + 1
        total_cand_score = 0
        for i in range(0,len(cand_score_list)):
            total_cand_score = total_cand_score + cand_score_list[i][0]
        print(f"Candidate {cand} was approved by:")
        for i in range(0,len(cand_score_list)):
            print(f"{cand_score_list[i][0]} voters on index {cand_score_list[i][1]} ballots,")
        print(f"{cand} received a total of {total_cand_score} votes.")
        print()

def approval_result_statement(profile):
    # Print winner or list of candidates who tied in approval election        
    if len(approval_results(profile)) ==1: 
        print(f"Candidate {approval_results(profile)[0]} won the election.")
    else:
        print(f"Candidates {approval_results(profile)} tied.")


def majority_question_approval(rank_profile, score_profile):
    #Asks whether approval election violates the Majority criterion.
    while True:
        answer = input("Did the approval election violate the Majority criterion? (y/n): ")
        if answer == 'y' or answer == 'n':
            break
        else:
            print("Invalid input")
    r = Approval(profile=score_profile).get_elected()[0]
    approval_winner, = r
    maj = majority_test(rank_profile)

    if maj != None:
        print("Answer: ",answer)
        print("The approval winner is:", approval_winner)
        print("The Majority candidate is:", maj)
        if r == maj:
            if answer == "n":
                print("Correct. The approval election did not violate the Majority criterion.")
            else:
                print("Incorrect. The approval election did not violate the Majority criterion.")
        elif r != maj:
            if answer == "y":
                print("Correct. The approval election violated the Majority criterion.")
            else:
                print("Incorrect. The approval election violated the Majority criterion.")  
    else:
        print("Answer: ",answer)
        print("The approval winner is:", approval_winner)
        print("There is no Majority candidate.")
        if answer == "n":
            print("Correct. The approval election did not violate the Majority criterion.")
        else:
            print("Incorrect. The approval election did not violate the Majority criterion.") 

#1992 election simulation

def get_votes_wp():
    pres = "CVR files/1992_US_Presidential_Election_with_Perot.csv"
    return pd.read_csv(pres, encoding="latin-1")

def get_votes_np():
    pres_np = "CVR files/1992_US_Presidential_Election_No_Perot.csv"
    return pd.read_csv(pres_np, encoding="latin-1")
    